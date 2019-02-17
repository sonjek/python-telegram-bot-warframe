#!/usr/bin/env python
# -*- coding: utf-8 -*-
#

import sys
import traceback
from telegram import ParseMode

from . import menus, keyboards
from ..sources import wf, twitch
from ..utils import utils
from ..utils.logging import logger
from ..utils.loadconfig import config

warframe = wf.Warframe()
tw = twitch.Twitch()


def error(update, context):
    trace = ''.join(traceback.format_tb(sys.exc_info()[2]))
    text = f'The error <code>{context.error}</code> happened. The full traceback:\n\n<code>{trace}</code>'
    context.bot.send_message(config['admin_id'], text, parse_mode=ParseMode.HTML)
    logger.error(f'Update: {update}')
    raise context.error


def start(update, context):
    utils.update_user_data(update.message.from_user, context.user_data)
    update.message.reply_text('Please choose:', reply_markup=keyboards.main_menu_keyboard())


def alerts(update, context):
    utils.update_user_data(update.message.from_user, context.user_data)
    update.message.reply_text(text=wf.get_alerts(), parse_mode=ParseMode.MARKDOWN)


def invasions(update, context):
    utils.update_user_data(update.message.from_user, context.user_data)
    text = wf.get_invasions(update.message.from_user.id, True, False)
    update.message.reply_text(text=text, parse_mode=ParseMode.MARKDOWN)


def void_trader(update, context):
    if update.message is not None:
        from_user = update.message.from_user
    else:
        from_user = update.callback_query.from_user

    utils.update_user_data(update.message.from_user, context.user_data)
    text = wf.get_void_trader_items(from_user.id)
    update.message.reply_text(text=text, parse_mode=ParseMode.MARKDOWN)


def twitch_get_channel_status(update, context):
    utils.update_user_data(update.message.from_user, context.user_data)
    text, info = tw.get_twitch_status(update.message.from_user.id)
    update.message.reply_text(text=text, parse_mode=ParseMode.MARKDOWN)


def admin(update, context):
    utils.update_user_data(update.message.from_user, context.user_data)
    menus.admin_menu(update, context)


def job_invasions(update):
    chat_id = update.job.context
    msg = warframe.get_invasions(chat_id, False, True)
    if msg and msg != wf.no_invasions_msg and msg != wf.no_invasions_rare_rewards_msg:
        update.bot.send_message(chat_id=chat_id, text=msg, parse_mode=ParseMode.MARKDOWN)


def job_alerts(update):
    chat_id = update.job.context
    msg = warframe.get_alerts(chat_id, True, True)
    if msg and msg != wf.no_alerts_msg:
        update.bot.send_message(chat_id=chat_id, text=msg, parse_mode=ParseMode.MARKDOWN)


def job_void_trader(update):
    chat_id = update.job.context
    msg = warframe.get_void_trader_items(chat_id, True)
    if msg:
        update.bot.send_message(chat_id=chat_id, text=msg, parse_mode=ParseMode.MARKDOWN)


def job_twitch_get_channel_status(update):
    chat_id = update.job.context
    text, info = tw.get_twitch_status(chat_id, True)
    if text and text != twitch.not_active_msg:
        update.bot.send_message(chat_id=chat_id, text=text, parse_mode=ParseMode.MARKDOWN)
