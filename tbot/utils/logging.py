#!/usr/bin/env python
# -*- coding: utf-8 -*-
#

from pathlib import Path
import logging
from logging.handlers import TimedRotatingFileHandler
from .loadconfig import config, get_path


logging.basicConfig(level=logging.DEBUG, format=config['log_format'], datefmt=config['date_time_format'])
logger = logging.getLogger()

if config['log_to_file']:
    log_dir = get_path('log_folder')
    Path(log_dir).mkdir(parents=True, exist_ok=True)

    file_path = log_dir.joinpath(config['log_file'])
    fl = TimedRotatingFileHandler(file_path, when='midnight', interval=1, backupCount=31)
    fl.setLevel(logging.INFO)
    formatter = logging.Formatter(config['log_format'])
    fl.setFormatter(formatter)
    logger.addHandler(fl)
