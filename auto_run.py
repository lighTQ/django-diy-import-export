#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
@author: HighWay.Li
@contact:byamian@gmail.com
@version: 1.0.0
@license: Apache Licence
@file: auto_run.py
@time: 12/1/24 PM9:47
"""

import os
import sys
import webbrowser
import  psutil
from core.settings import HOSTNAME,PORT

BASE_PATH = os.path.abspath('')

os.system('TASKKILL /F /IM manage.exe')

def run_main():
    # sys.path.append("libs")
    url=f"{HOSTNAME}:{PORT}"
    main = BASE_PATH+f"/okApp runserver {HOSTNAME}:{PORT} --noreload"
    print('_____')
    print('server is running!!')
    print('_____')
    os.system(main)
run_main()