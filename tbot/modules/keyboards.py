#!/usr/bin/env python
# -*- coding: utf-8 -*-
#

from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from ..utils import utils


def main_menu_keyboard():
    keyboard = [
        [InlineKeyboardButton('All Invasions', callback_data='allInvasions'),
         InlineKeyboardButton('Rare Invasions', callback_data='rareInvasions')],
        [InlineKeyboardButton('All Active Alerts', callback_data='alertsList')],
        [InlineKeyboardButton('Void Trader Items', callback_data='itemsList'),
         InlineKeyboardButton('Void Trader Period', callback_data='timePeriod')],
        [InlineKeyboardButton('Twitch Channel Status', callback_data='twitchStatus')]
    ]
    return InlineKeyboardMarkup(keyboard)


def admin_menu_keyboard(job_names):
    invasions_title, invasions_code = utils.prepare_switch_button(job_names, 'job_invasion_notification')
    alerts_title, alerts_code = utils.prepare_switch_button(job_names, 'job_alert_notification')
    void_trader_title, void_trader_code = utils.prepare_switch_button(job_names, 'job_void_trader_notification')
    tw_status_title, tw_status_code = utils.prepare_switch_button(job_names, 'job_twitch_channel_status_notification')

    keyboard = [
        [InlineKeyboardButton(invasions_title + 'Invasions Notifications', callback_data=invasions_code),
         InlineKeyboardButton(alerts_title + 'Alerts Notifications', callback_data=alerts_code)],
        [InlineKeyboardButton(void_trader_title + 'Void Trader Notifications', callback_data=void_trader_code),
         InlineKeyboardButton(tw_status_title + 'Twitch Status Notifications', callback_data=tw_status_code)],
        [InlineKeyboardButton('Main Menu', callback_data='menu')]
    ]
    return InlineKeyboardMarkup(keyboard)
