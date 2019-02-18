#!/usr/bin/env python
# -*- coding: utf-8 -*-
#

from telegram.ext import CommandHandler, InlineQueryHandler, Filters, CallbackQueryHandler
from datetime import timedelta

from ..utils import jobpickle
from . import commands, menus, buttons, inlinequery
from ..utils.loadconfig import config


def init(updater):
    dispatcher = updater.dispatcher

    updater.job_queue.run_repeating(jobpickle.save_jobs_job, timedelta(minutes=config['backup_job_minutes_interval']))

    dispatcher.add_error_handler(commands.error)

    dispatcher.add_handler(CommandHandler('admin', commands.admin, filters=Filters.user(username=config['admin_name'])))
    dispatcher.add_handler(CommandHandler('start', commands.start))
    dispatcher.add_handler(CommandHandler('invasions', commands.invasions))
    dispatcher.add_handler(CommandHandler('alerts', commands.alerts))
    dispatcher.add_handler(CommandHandler('voidtrader', commands.void_trader))
    dispatcher.add_handler(CommandHandler('twitchstatus', commands.twitch_get_channel_status, pass_user_data=True))

    dispatcher.add_handler(CallbackQueryHandler(menus.main_menu, pattern='^menu$'))
    dispatcher.add_handler(CallbackQueryHandler(buttons.button, pass_job_queue=True, pass_update_queue=True))
    dispatcher.add_handler(InlineQueryHandler(inlinequery.warframe_inline_query, pattern='^wf$'))
