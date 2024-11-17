#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
@author: HighWay.Li
@contact:byamian@gmail.com
@version: 1.0.0
@license: Apache Licence
@file: forms.py
@time: 11/17/24 PM3:07
"""

from django import forms
class ImportFileForm(forms.Form):
    file = forms.FileField()
    add_params= forms.CharField(max_length=100)
