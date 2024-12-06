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
from api.views import config_view,general_util_view ,file_upload_view
from core.settings import HOSTNAME,PORT
# 自动生成的路由必须继承ViewSetMixin，才能自动生成
router = SimpleRouter()
router.register('configInfo', config_view.ConfigModelView)


urlpatterns = [
    path('getDropDown',general_util_view.GeneralUtilViewSet.as_view({'get':'dropDown'}),name='getDropDown'),
    path('uploadPics', file_upload_view.FileUploadView.as_view({'post': 'uploadPics'}), name='uploadPics'),
    path('', include(router.urls)),
]
print('route: \n')
print(router.urls)

#from api.runapscheduler import start_scheduler
# start_scheduler()

import webbrowser
webbrowser.open(f'http://{HOSTNAME}:{PORT}')