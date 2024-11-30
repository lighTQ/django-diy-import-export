#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
@author: HighWay.Li
@contact:byamian@gmail.com
@version: 1.0.0
@license: Apache Licence
@file: admin.py
@time: 11/21/24 PM6:36
"""
from django.contrib import admin
from api.models.models import *
admin.site.register(Person)
admin.site.register(CONFIG_INFO)