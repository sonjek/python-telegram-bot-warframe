#!/usr/bin/env python
# -*- coding: utf-8 -*-
#

import requests
from datetime import datetime, timedelta

from ..utils.Singleton import Singleton
from ..utils.loadconfig import config
from ..utils.logging import logger
from ..utils import db

not_active_msg = 'Translation is not active'


class Twitch(metaclass=Singleton):
    def __init__(self):
        self.cache_lifetime = config['source_cache_minutes_interval']

        self.info = None
        self.status = 'error'
        self.max_channel_state_store_time = None

    def update_channel_state(self):
        try:
            url = config['twitch_endpoint']
            logger.info(f'@@@@ update_channel_state from {url}')
            r = requests.get(url, headers={'Client-ID': config['twitch_token']}, timeout=15)

            try:
                info = r.json()
            except UnicodeDecodeError as e:
                logger.error(f'Invalid JSON passed: {r.content}')
                raise e

            if info['stream'] is None:
                self.status = 'offline'
            else:
                self.status = 'online'
            self.info = info['stream']
        except requests.exceptions.RequestException as e:
            if e.response:
                if e.response.reason == 'Not Found' or e.response.reason == 'Unprocessable Entity':
                    self.status = 'not found'
        self.max_channel_state_store_time = datetime.now() + timedelta(minutes=self.cache_lifetime)

    def prepare_data(self):
        if not self.max_channel_state_store_time or self.max_channel_state_store_time < datetime.now():
            self.update_channel_state()

        if self.status is 'online':
            info = {
                'id': self.info['_id'],
                'created': self.info['created_at'],
                'title': self.info['channel']['status'],
                'prev': self.info['preview']['medium'],
                'url': self.info['channel']['url']
            }
            text = f"[link]({info['url']}) {info['title']}"
        else:
            info = self.info
            text = not_active_msg
        return info, text

    def get_twitch_status(self, user_id, is_job=False):
        logger.info(f'@@@@ get_twitch_status for {user_id}')

        info, text = self.prepare_data()

        msg = ''
        if text and text != not_active_msg and is_job and user_id:
            if db.is_twitch_status_notified(info['id'], user_id):
                logger.debug(f"@@@@ skip notified twitch_status for {user_id} >> {info['title']}")
                text = not_active_msg
            else:
                db.put_twitch_status(info['id'], info['created'], info['title'], user_id)
        msg += text

        return msg, info


def get_twitch_status(user_id=None):
    return Twitch().get_twitch_status(user_id)
