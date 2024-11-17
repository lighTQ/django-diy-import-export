#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
@author: HighWay.Li
@contact:byamian@gmail.com
@version: 1.0.0
@license: Apache Licence
@file: s.py
@time: 11/17/24 PM9:45
"""
class Test():
    def list(self):
        print("ssss")

## python reflected
test = Test()
l=getattr(test,'list')
setattr(test,'get',l)
test.get()
