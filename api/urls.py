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

from django.urls import path
from . import views
urlpatterns = [
    path('goods/', views.goods_list),
    path('goods/<int:id>', views.goods_detail),
    path('publish/',views.PublishViewSet.as_view({'get': 'list', 'post': 'create'})),
    path('book1/',views.Book.as_view()),
    path('book2/',views.BookAPIView.as_view()),
]
