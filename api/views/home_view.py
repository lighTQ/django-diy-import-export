#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
@author: HighWay.Li
@contact:byamian@gmail.com
@version: 1.0.0
@license: Apache Licence
@file: homeView.py
@time: 11/25/24 PM8:30
"""
from django.shortcuts import render
from rest_framework.views import APIView


class HomePageView(APIView):
    def get(self, request,*args,**kwargs):
        return render(request, 'home_page.html')

    def index(self,request,*args,**kwargs):
        return render(request, 'index.html')