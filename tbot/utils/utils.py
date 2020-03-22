#!/usr/bin/env python
# -*- coding: utf-8 -*-
#

from .loadconfig import config
from .logging import logger
from . import db


def prepare_and_save_user_data(user_id, username, first_name, last_name, language):
    current_user_data = {
        'id': user_id,
        'username': username,
        'first_name': first_name,
        'last_name': last_name,
        'language': language
    }

    saved_user_info = db.get_user_data(user_id)
    if not saved_user_info:
        logger.info(f'@@@@ creating data for user_id {user_id}, username {username}')
        db.put_user_data(user_id, current_user_data)
    elif saved_user_info[0] != current_user_data:
        logger.info(f'@@@@ updating data for user_id {user_id}, old data {saved_user_info[0]}')
        db.put_user_data(user_id, current_user_data)

    return current_user_data


def update_user_data(user_info, user_data):
    db_user_data = prepare_and_save_user_data(
        user_info.id,
        user_info.username,
        user_info.first_name,
        user_info.last_name,
        user_info.language_code
    )

    if user_data != db_user_data:
        user_data.update(db_user_data)


def prepare_switch_button(job_names, job_name):
    job_code = config[job_name]
    state = job_code in job_names
    title = '✓ ' if state else '✗ '
    code = ('remove_' if state else 'schedule_') + job_code
    return title, code
