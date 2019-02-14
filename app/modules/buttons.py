#!/usr/bin/env python
# -*- coding: utf-8 -*-
#

from telegram import ParseMode

from ..sources import wf


def button(update, context):
    used_id = update.callback_query.message.chat.id
    query = update.callback_query
    if query.data == 'allInvasions':
        msg = wf.get_invasions(used_id, True, False)
        query.edit_message_text(text=msg, parse_mode=ParseMode.MARKDOWN)
    elif query.data == 'rareInvasions':
        msg = wf.get_invasions(used_id, False, False)
        query.edit_message_text(text=msg, parse_mode=ParseMode.MARKDOWN)

    else:
        query.edit_message_text(text=f'Selected option: {query.data}')
