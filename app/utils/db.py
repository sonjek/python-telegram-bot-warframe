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
