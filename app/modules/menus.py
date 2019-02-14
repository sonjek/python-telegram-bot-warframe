#!/usr/bin/env python
# -*- coding: utf-8 -*-
#

from . import keyboards
from ..utils.logging import logger


def main_menu(update, context):
    logger.info(f'@@@@ user_data {context.user_data}')

    query = update.callback_query
    context.bot.edit_message_text(chat_id=query.message.chat_id,
                                  message_id=query.message.message_id,
                                  text='Please choose action:',
                                  reply_markup=keyboards.main_menu_keyboard())
