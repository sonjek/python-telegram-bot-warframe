#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# https://tinydb.readthedocs.io/en/latest/
#

from tinydb import TinyDB, Query

from .loadconfig import get_path
from .logging import logger

db = TinyDB(get_path('dbfile'), sort_keys=True, indent=4, separators=(',', ': '))


def get_user_data(user_id):
    if user_id:
        logger.debug(f'@@@@ [{user_id}] get data')
        User = Query()
        users = db.table('users')
        return users.search(User.id == user_id)


def put_user_data(user_id, user_data):
    User = Query()

    users = db.table('users')
    if users.contains(User.id == user_id):
        logger.debug(f'@@@@ [{user_id}] update data {user_data}')
        users.update(user_data, User.id == user_id)
    else:
        logger.debug(f'@@@@ [{user_id}] insert data {user_data}')
        users.insert(user_data)


def is_alert_notified(alert_id, user_id):
    Alert = Query()

    alerts = db.table('alerts')
    if alerts.contains(Alert.id == alert_id):
        alert_list = alerts.search(Alert.id == alert_id)
        if not alert_list:
            logger.debug(f'@@@@ [{user_id}] isAlertNotified FALSE 1 for {alert_id}')
            return False
        else:
            users = alert_list[0]['users']
            if user_id not in users:
                logger.debug(f'@@@@ [{user_id}] isAlertNotified FALSE 2 for {alert_id}')
                return False
            else:
                logger.debug(f'@@@@ [{user_id}] isAlertNotified True for {alert_id}')
                return True
    else:
        logger.debug(f'@@@@ [{user_id}] isAlertNotified FALSE 3 for {alert_id}')
        return False


def put_alert(alert_id, user_id, reward, created):
    Alert = Query()

    alerts = db.table('alerts')
    if not alerts.contains(Alert.id == alert_id):
        alert = {'id': alert_id, 'created': created, 'reward': reward, 'users': [user_id]}
        logger.debug(f'@@@@ [{user_id}] insert alert {alert_id} -> {alert}')
        alerts.insert(alert)
    else:
        alert_list = alerts.search(Alert.id == alert_id)
        if alert_list:
            alert = alert_list[0]
            logger.debug(f'@@@@ [{user_id}] alert {alert_id} --->>> {alert}')
            users = alert['users']
            if user_id not in users:
                users.append(user_id)

                alerts.update({'users': users}, Alert.id == alert_id)
                logger.debug(f'@@@@ [{user_id}] alert {alert_id} update users {users}')


def is_invasion_notified(invasion_id, user_id):
    Invasion = Query()

    invasions = db.table('invasions')
    if invasions.contains((Invasion.id == invasion_id) & (Invasion.started == True) & (Invasion.users.any([user_id]))):
        logger.debug(f'@@@@ [{user_id}] isInvasionNotified TRUE for {invasion_id}')
        return True
    else:
        logger.debug(f'@@@@ [{user_id}] isInvasionNotified FALSE for {invasion_id}')
        return False


def put_invasion(invasion_id, user_id, reward_a, reward_d, created, started):
    Invasion = Query()

    invasions = db.table('invasions')
    if not invasions.contains(Invasion.id == invasion_id):
        invasion = {'id': invasion_id, 'created': created, 'started': started,
                    'reward_a': reward_a, 'reward_d': reward_d, 'users': [user_id]}
        logger.debug(f'@@@@ [{user_id}] insert invasion {invasion_id} -> {invasion}')
        invasions.insert(invasion)
    else:
        invasion_list = invasions.search(Invasion.id == invasion_id)
        if invasion_list:
            invasion = invasion_list[0]
            logger.debug(f'@@@@ [{user_id}] inv {invasion_id} --->>> {invasion}')
            users = invasion['users']
            if user_id not in users:
                users.append(user_id)
                invasions.update({'users': users}, Invasion.id == invasion_id)
                logger.debug(f'@@@@ [{user_id}] inv {invasion_id} update users {users}')
            if not invasion['started'] and started:
                invasions.update({'started': started}, Invasion.id == invasion_id)
                logger.debug(f'@@@@ [{user_id}] inv {invasion_id} update started {started}')


def is_void_trader_item_notified(item_id, user_id):
    """
    # & (Voidtrader.inventory.any(Inventory.num == item))
    """
    Voidtrader = Query()

    void_trader_items = db.table('void_trader')
    void_trader_items_list = void_trader_items.search((Voidtrader.id == item_id) & (Voidtrader.users.any([user_id])))
    if void_trader_items_list:
        logger.debug(f'@@@@ [{user_id}] isVoidTraderItemNotified TRUE for {item_id}')
        return True
    else:
        logger.debug(f'@@@@ [{user_id}] isVoidTraderItemNotified FALSE for {item_id}')
        return False


def put_void_trader_item(item_id, user_id, inventory):
    Voidtrader = Query()

    void_trader_items = db.table('void_trader')
    void_trader_items_list = void_trader_items.search(Voidtrader.id == item_id)

    if not void_trader_items_list:
        void_trader_item = {'id': item_id, 'inventory': inventory, 'users': [user_id]}
        logger.debug(f'@@@@ [{user_id}] insert VoidTrader Item {item_id} -> {void_trader_item}')

        void_trader_items.insert(void_trader_item)
    else:
        void_trader_item = void_trader_items_list[0]
        is_need_update = False

        users = void_trader_item['users']
        if user_id not in users:
            users.append(user_id)
            is_need_update = True

        if is_need_update:
            void_trader_items.update(void_trader_item, Voidtrader.id == item_id)
            logger.debug(f'@@@@ [{user_id}] update VoidTrader Item {item_id} -> {void_trader_item}')
