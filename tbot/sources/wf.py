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
from .wf_alert import Alert
from .wf_void_trader import Baro


no_alerts_msg = 'No active alerts'
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

        self.alerts = []
        self.max_alerts_store_time = None

        self.invasions = []
        self.max_invasions_store_time = None

        self.void_trader = None
        self.max_void_trader_store_time = None

    def prepare_alerts(self):
        if not self.max_alerts_store_time or self.max_alerts_store_time < datetime.now():
            alerts_json = get_json(config['api_alerts'])

            alerts = []
            for alertNum in range(len(alerts_json)):
                alerts.append(Alert(alertNum, **alerts_json[alertNum]))

            self.alerts = sorted(alerts, key=lambda x: (x.planet, x.location))
            self.max_alerts_store_time = datetime.now() + timedelta(minutes=self.cache_lifetime)

    def prepare_invasions(self):
        if not self.invasions or self.max_invasions_store_time < datetime.now():
            invasions = get_json(config['api_invasions'])

            self.invasions = []
            for invasionNum in range(len(invasions)):
                self.invasions.append(Invasion(invasionNum, **invasions[invasionNum]))
            self.invasions = sorted(self.invasions, key=lambda x: (x.planet, x.completion))
            self.max_invasions_store_time = datetime.now() + timedelta(minutes=self.cache_lifetime)

    def prepare_void_trader(self):
        if not self.void_trader or self.max_void_trader_store_time < datetime.now():
            void_trader = get_json(config['api_void_trader'])
            if void_trader:
                self.void_trader = Baro(**void_trader)
                self.max_void_trader_store_time = datetime.now() + timedelta(minutes=self.cache_lifetime)

    def get_alerts(self, user_id=None, markdown=True, is_job=False):
        logger.info(f'@@@@ get_alerts for {user_id}')
        self.prepare_alerts()

        msg = ''
        for y in range(len(self.alerts)):
            alert_id, text, reward, created = self.alerts[y].get_alert(markdown)

            if is_job and user_id:
                if db.is_alert_notified(alert_id, user_id):
                    logger.debug(f'@@@@ skip notified alert {alert_id} for {user_id} >> {reward}')
                    text = ''
                else:
                    db.put_alert(alert_id, user_id, reward, created)
            msg += text
        return msg

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

    def get_void_trader_info(self, user_id=None):
        logger.info(f'@@@@ get_void_trader_info for {user_id}')
        self.prepare_void_trader()
        return self.void_trader.get_baro()

    def get_void_trader_items(self, user_id=None, is_job=False):
        logger.info(f'@@@@ get_void_trader_items for {user_id}')
        self.prepare_void_trader()

        void_trader = self.void_trader
        if not void_trader.active and not is_job:
            return void_trader.get_baro()
        if not void_trader.active and is_job:
            return None

        result = ''
        if is_job and user_id and db.is_void_trader_item_notified(void_trader.activation, user_id):
            logger.debug(f'@@@@ skip notified void trader {void_trader.activation} for {user_id}')
            return result

        items = []
        for y in range(len(void_trader.inventory)):
            lot = void_trader.inventory[y]
            items.append(f"{lot['item']} - ducats {lot['ducats']}, credits {lot['credits']}")

        if items:
            if is_job and user_id and not db.is_void_trader_item_notified(void_trader.activation, user_id):
                db.put_void_trader_item(void_trader.activation, user_id, items)

            result = void_trader.get_baro() + '\n\n' + '\n'.join(items)
        return result


def get_alerts(user_id=None, is_job=False):
    msg = Warframe().get_alerts(user_id, is_job)
    if not msg:
        msg = no_alerts_msg
    return msg


def get_invasions(user_id=None, all_active=True, is_job=False):
    msg = Warframe().get_invasions(user_id, all_active, is_job)
    if not msg:
        msg = no_invasions_msg if all_active else no_invasions_rare_rewards_msg
    return msg


def get_void_trader_info(user_id=None):
    return Warframe().get_void_trader_info(user_id)


def get_void_trader_items(user_id=None, is_job=False):
    return Warframe().get_void_trader_items(user_id, is_job)
