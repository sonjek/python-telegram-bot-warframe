#!/usr/bin/env python
# -*- coding: utf-8 -*-
#

from pathlib import Path
import json

DATA_DIR = 'data'
CONFIG_FILE = 'config.json'

config_file_dir = Path('./').joinpath(DATA_DIR)
if not config_file_dir.is_dir():
    config_file_dir = Path('../').joinpath(DATA_DIR)

config_file_path = config_file_dir.joinpath(CONFIG_FILE)

if config_file_path.is_file():
    with open(config_file_path) as config_file:
        config = json.load(config_file)
        config['data_folder'] = config_file_dir
else:
    exit(f'No configuration file {CONFIG_FILE} found in dir {config_file_dir.absolute().resolve()}')


def get_path(config_var_name):
    return config['data_folder'].joinpath(config[config_var_name])
