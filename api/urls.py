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
from . import generic_view,config_view
# 自动生成的路由必须继承ViewSetMixin，才能自动生成

router = SimpleRouter()
# router.register(r'books', generic_view.BookView3)
router.register('configInfo', config_view.ConfigModelView)

urlpatterns = [

    path('',include(router.urls)),
    # 自动生成的路由可以设置路径
    # path('api/v1',include(router.urls)),

    # path('goods/', views.goods_list),
    # path('goods/<int:id>', views.goods_detail),
    # # path('publish/', views.PublishViewSet.as_view({'get': 'list', 'post': 'create'})),
    # path('book1/', views.Book.as_view()),
    # # path('book2/', views.BookAPIView.as_view()),
    # path('books/', views.BookAPIView.as_view()),
    # # path('books/<str:name>/<int:price>', views.BookDetailAPIView.as_view()),
    # path('books/<str:name>', views.BookDetailAPIView.as_view()),
    # path('publish/',views.PublishView.as_view()),
    #
    # path('export/',views.ExportExcelView.as_view()),
    #
    # path('import/',views.ImportExcelView.as_view()),
    # path('import_file/',views.ImportFileView.as_view()),
    # path('export_file/',views.ExportFileView.as_view()),
    #
    # path('g_publish/',generic_view.PublishGenericAPIView.as_view()),
    # path('g_publish/<str:name>',generic_view.PublishDetailGenericAPIView.as_view()),
    #
    # path('g_books/',generic_view.BookGenericAPIView.as_view()),
    # path('g_books/<str:name>',generic_view.BookDetailGenericAPIView.as_view()),
    #
    # path('gg_books/',generic_view.BookView2.as_view()),
    # path('gg_books/<str:name>',generic_view.Book2DetailView.as_view()),
    #
    # path('ggg_books/',generic_view.BookView3.as_view({'get':'list','post':'create'})),
    # path('ggg_books/<str:name>',generic_view.BookView3.as_view({'get':'retrieve','put':'update','delete':'destroy'})),
    path('index_home/<str:name>',generic_view.IndexView.as_view({'get':'lhw'}))
]

print(router.urls)
from  api.runapscheduler import start_scheduler

start_scheduler()