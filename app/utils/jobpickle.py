#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# https://github.com/python-telegram-bot/python-telegram-bot/wiki/Making-your-bot-persistent
# https://github.com/python-telegram-bot/python-telegram-bot/wiki/Code-snippets#save-and-load-jobs-using-pickle
#

import pickle
from telegram.ext import Job
from time import time

from .loadconfig import get_path
from .logging import logger


JOB_DATA = ('callback', 'interval', 'repeat', 'context', 'days', 'name', 'tzinfo')
JOB_STATE = ('_remove', '_enabled')


def load_jobs(jq):
    with open(get_path('job_pickle_db'), 'rb') as fp:
        while True:
            try:
                next_t, data, state = pickle.load(fp)
            except EOFError:
                break  # Loaded all job tuples

            # New object with the same data
            job = Job(**{var: val for var, val in zip(JOB_DATA, data)})

            # Restore the state it had
            for var, val in zip(JOB_STATE, state):
                attribute = getattr(job, var)
                getattr(attribute, 'set' if val else 'clear')()

            job.job_queue = jq

            next_t -= time()  # convert from absolute to relative time

            jq._put(job, next_t)
            logger.info(f'@@@@ {job.name} RESTORED, interval={job.interval}')


def save_jobs(jq):
    with jq._queue.mutex:  # in case job_queue makes a change

        if jq:
            job_tuples = jq._queue.queue
        else:
            job_tuples = []

        with open(get_path('job_pickle_db'), 'wb') as fp:
            for next_t, job in job_tuples:

                # This job is always created at the start
                if job.name == 'save_jobs_job':
                    continue

                # Threading primitives are not pickleable
                data = tuple(getattr(job, var) for var in JOB_DATA)
                state = tuple(getattr(job, var).is_set() for var in JOB_STATE)

                # Pickle the job
                pickle.dump((next_t, data, state), fp)
                logger.debug(f'@@@@ {job.name} DUMPED, interval={job.interval}')
    logger.info(f'@@@@ save_jobs DONE')


def save_jobs_job(context):
    save_jobs(context.job_queue)
