#!/usr/bin/env python
# -*- coding: utf-8 -*-
#

from telegram import InlineKeyboardButton, InlineKeyboardMarkup


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
