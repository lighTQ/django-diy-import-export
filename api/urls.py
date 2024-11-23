#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
@author: HighWay.Li
@contact:byamian@gmail.com
@version: 1.0.0
@license: Apache Licence
@file: urls.py
@time: 11/15/24 PM7:04
"""

from django.urls import path, include
from rest_framework.routers import SimpleRouter
from api import (config_view)

# 自动生成的路由必须继承ViewSetMixin，才能自动生成
router = SimpleRouter()
router.register('configInfo', config_view.ConfigModelView)

urlpatterns = [
    path('', include(router.urls)),
]

print('route: \n')
print(router.urls)

from api.runapscheduler import start_scheduler  # start_scheduler()
