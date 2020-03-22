#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# https://python-telegram-bot.readthedocs.io/en/stable/telegram.html
# https://github.com/python-telegram-bot/python-telegram-bot
#
# https://api.telegram.org/bot____:_____/getUpdates
#

from telegram.ext import Updater, PicklePersistence
from tbot.modules import dispatcher
from tbot.utils.loadconfig import config, get_path
from tbot.utils import jobpickle


def main():
    pp = PicklePersistence(filename=get_path('pickle_persistence_db'))
    updater = Updater(token=config['bot_token'], persistence=pp, use_context=True)

    try:
        jobpickle.load_jobs(updater.job_queue)
    except FileNotFoundError:
        pass

    dispatcher.init(updater)

    updater.start_polling(clean=True)
    updater.idle()

    jobpickle.save_jobs(updater.job_queue)


if __name__ == '__main__':
    main()
