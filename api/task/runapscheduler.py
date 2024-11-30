#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
@author: HighWay.Li
@contact:byamian@gmail.com
@version: 1.0.0
@license: Apache Licence
@file: diyTask.py
@time: 11/20/24 PM7:07
"""
import logging
from datetime import datetime, timezone

from threading import Lock

from apscheduler.schedulers.background import BackgroundScheduler

lock = Lock()
scheduler = BackgroundScheduler()
logger = logging.getLogger(__name__)

# start jobScheduler

def start_scheduler():
    global scheduler
    if not scheduler.running:
        try:
            scheduler.add_job(my_task1, 'interval', seconds=5, id='my_task1', replace_existing=True, max_instances=1,
                              coalesce=True)
            scheduler.add_job(my_task2, 'interval', seconds=5, id='my_task2', replace_existing=True, max_instances=1,
                              coalesce=True)

            print('start start_scheduler....')
            scheduler.start()
            print('start_scheduler ok ')
        except Exception as e:
            print('start_scheduler error', e)
            scheduler.shutdown()




def my_task1():
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print("my_task is running at:{}".format(ts))


def my_task2():
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print("my_task2 is running at:{}".format(ts))
