#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# https://python-telegram-bot.readthedocs.io/en/stable/telegram.html
# https://github.com/python-telegram-bot/python-telegram-bot
#
# https://api.telegram.org/bot____:_____/getUpdates
#

from telegram.ext import Updater, PicklePersistence
from app.modules import dispatcher
from app.utils.loadconfig import config, get_path


def main():
    pp = PicklePersistence(filename=get_path('pickle_persistence_db'))
    updater = Updater(token=config['bot_token'], persistence=pp, use_context=True)

    dispatcher.init(updater)

    updater.start_polling(clean=True)
    updater.idle()


if __name__ == '__main__':
    main()
