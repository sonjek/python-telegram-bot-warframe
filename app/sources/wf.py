#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# https://warframestat.us/
# https://docs.warframestat.us/
# https://deathsnacks.com/wf/index.html
# http://content.warframe.com/dynamic/worldState.php
#

import requests

from datetime import datetime, timedelta

from ..utils.Singleton import Singleton
from ..utils.loadconfig import config
from ..utils.logging import logger
from ..utils import db

from .wf_invasion import Invasion


no_invasions_msg = 'No active invasions'
no_invasions_rare_rewards_msg = 'No active invasions with rare reward'


def get_json(key):
    url = config['api_endpoint'] + key
    logger.info(f'@@@@ get_json get data from {url}')
    r = requests.get(url, timeout=15)

    status = r.status_code
    if status != 200:
        logger.error(f'Error communicating with Warframe servers. url: {url}, status: {status}')

    try:
        data = r.json()
    except UnicodeDecodeError as e:
        logger.error(f'Invalid JSON passed: {r.content}')
        raise e
    return data


class Warframe(metaclass=Singleton):
    def __init__(self):
        self.cache_lifetime = config['source_cache_minutes_interval']

        self.invasions = []
        self.max_invasions_store_time = None

    def prepare_invasions(self):
        if not self.invasions or self.max_invasions_store_time < datetime.now():
            invasions = get_json(config['api_invasions'])

            self.invasions = []
            for invasionNum in range(len(invasions)):
                self.invasions.append(Invasion(invasionNum, **invasions[invasionNum]))
            self.invasions = sorted(self.invasions, key=lambda x: (x.planet, x.completion))
            self.max_invasions_store_time = datetime.now() + timedelta(minutes=self.cache_lifetime)

    def get_invasions(self, user_id=None, all_active=True, is_job=False):
        logger.info(f'@@@@ get_invasions for {user_id}')
        self.prepare_invasions()

        msg = ''
        for y in range(len(self.invasions)):
            id, is_rare, text, reward_a, reward_d, created, started = self.invasions[y].get_invasion(all_active, is_job)
            if is_rare and user_id:
                if is_job and db.is_invasion_notified(id, user_id):
                    logger.debug(f'@@@@ skip notified {id} for {user_id} >> {reward_a} and {reward_d}')
                    text = ''
                if is_job:
                    db.put_invasion(id, user_id, reward_a, reward_d, created, started)
                    if not started:
                        logger.debug(f'@@@@ skip not started {id} for {user_id} >> {reward_a} and {reward_d}')
                        text = ''
            msg += text
        return msg


def get_invasions(user_id=None, all_active=True, is_job=False):
    msg = Warframe().get_invasions(user_id, all_active, is_job)
    if not msg:
        msg = no_invasions_msg if all_active else no_invasions_rare_rewards_msg
    return msg
