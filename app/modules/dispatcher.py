#!/usr/bin/env python
# -*- coding: utf-8 -*-
#

from telegram.ext import CommandHandler, InlineQueryHandler, CallbackQueryHandler

from . import commands, menus, buttons


def init(updater):
    dispatcher = updater.dispatcher

    dispatcher.add_error_handler(commands.error)

    dispatcher.add_handler(CommandHandler('start', commands.start))
    dispatcher.add_handler(CommandHandler('invasions', commands.invasions))
    dispatcher.add_handler(CommandHandler('alerts', commands.alerts))
    dispatcher.add_handler(CommandHandler('voidtrader', commands.void_trader))

    dispatcher.add_handler(CallbackQueryHandler(menus.main_menu, pattern='^menu$'))
    dispatcher.add_handler(CallbackQueryHandler(buttons.button, pass_job_queue=True, pass_update_queue=True))
    dispatcher.add_handler(InlineQueryHandler(inlinequery.warframe_inline_query, pattern='^wf$'))
