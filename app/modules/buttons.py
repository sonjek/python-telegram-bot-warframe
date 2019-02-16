#!/usr/bin/env python
# -*- coding: utf-8 -*-
#

from telegram import ParseMode

from ..sources import wf, twitch


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


    else:
        query.edit_message_text(text=f'Selected option: {query.data}')
