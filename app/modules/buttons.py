#!/usr/bin/env python
# -*- coding: utf-8 -*-
#

from telegram import ParseMode

from ..utils.loadconfig import config
from . import commands, schedule
from ..sources import wf, twitch


ALERT_CODE = config['job_alert_notification']
INVASION_CODE = config['job_invasion_notification']
VOID_TRADER_CODE = config['job_void_trader_notification']
TWITCH_STATUS_CODE = config['job_twitch_channel_status_notification']


def check_schedule_command(expected, job_code):
    return expected == 'schedule_' + job_code


def check_remove_command(expected, job_code):
    return expected == 'remove_' + job_code


def button(update, context):
    used_id = update.callback_query.message.chat.id
    query = update.callback_query
    if query.data == 'allInvasions':
        msg = wf.get_invasions(used_id, True, False)
        query.edit_message_text(text=msg, parse_mode=ParseMode.MARKDOWN)
    elif query.data == 'rareInvasions':
        msg = wf.get_invasions(used_id, False, False)
        query.edit_message_text(text=msg, parse_mode=ParseMode.MARKDOWN)
    elif query.data == 'alertsList':
        query.edit_message_text(text=wf.get_alerts(), parse_mode=ParseMode.MARKDOWN)
    elif query.data == 'itemsList':
        msg = wf.get_void_trader_items(used_id, False)
        query.edit_message_text(text=msg, parse_mode=ParseMode.MARKDOWN)
    elif query.data == 'timePeriod':
        msg = wf.get_void_trader_info(used_id)
        query.edit_message_text(text=msg, parse_mode=ParseMode.MARKDOWN)
    elif query.data == 'twitchStatus':
        text, info = twitch.get_twitch_status(used_id)
        query.edit_message_text(text=text, parse_mode=ParseMode.MARKDOWN)

    elif check_schedule_command(query.data, INVASION_CODE):
        schedule.schedule_notifications(update, context, INVASION_CODE, commands.job_invasions)
    elif check_schedule_command(query.data, ALERT_CODE):
        schedule.schedule_notifications(update, context, ALERT_CODE, commands.job_alerts)
    elif check_schedule_command(query.data, VOID_TRADER_CODE):
        schedule.schedule_notifications(update, context, VOID_TRADER_CODE, commands.job_void_trader)
    elif check_schedule_command(query.data, TWITCH_STATUS_CODE):
        schedule.schedule_notifications(update, context, TWITCH_STATUS_CODE, commands.job_twitch_get_channel_status)

    elif check_remove_command(query.data, INVASION_CODE):
        schedule.remove_job(update, context, INVASION_CODE, 'Invasions')
    elif check_remove_command(query.data, ALERT_CODE):
        schedule.remove_job(update, context, ALERT_CODE, 'Alerts')
    elif check_remove_command(query.data, VOID_TRADER_CODE):
        schedule.remove_job(update, context, VOID_TRADER_CODE, 'Void Trader')
    elif check_remove_command(query.data, TWITCH_STATUS_CODE):
        schedule.remove_job(update, context, TWITCH_STATUS_CODE, 'Twitch Channel Status')

    else:
        query.edit_message_text(text=f'Selected option: {query.data}')
