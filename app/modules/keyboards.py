#!/usr/bin/env python
# -*- coding: utf-8 -*-
#

from telegram import InlineKeyboardButton, InlineKeyboardMarkup


def main_menu_keyboard():
    keyboard = [
        [InlineKeyboardButton('All Invasions', callback_data='allInvasions'),
         InlineKeyboardButton('Rare Invasions', callback_data='rareInvasions')]
    ]
    return InlineKeyboardMarkup(keyboard)
