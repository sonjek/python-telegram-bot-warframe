#!/usr/bin/env python
# -*- coding: utf-8 -*-
#

from ..utils.loadconfig import config
from ..utils.logging import logger


def schedule_notifications(update, context, job_code, job, channel_id=config['channel_id']):
    interval = config['notifications_interval']
    jobs = context.job_queue.get_jobs_by_name(job_code)

    if len(jobs) == 0:
        context.job_queue.run_repeating(job, interval=interval, first=interval, context=channel_id, name=job_code)
        msg = f'{job_code} notification interval for {channel_id} scheduled to: {interval} seconds.'
    else:
        msg = f'{job_code} notification already scheduled for {channel_id} with interval: {jobs[0].interval} seconds.'

    update.callback_query.edit_message_text(msg)


def remove_job(update, context, job_code, job_title):
    jobs = context.job_queue.get_jobs_by_name(job_code)

    if len(jobs) > 0:
        for y in range(len(jobs)):
            job = jobs[y]
            logger.info(f'@@@@ Removing {job_code} ({job.name}) with interval={job.interval}')
            job.schedule_removal()
        msg = job_title + ' notifications disabled.'
    else:
        logger.info(f'@@@@ Job {job_code} already disabled')
        msg = job_title + ' notifications already disabled.'

    update.callback_query.edit_message_text(msg)
