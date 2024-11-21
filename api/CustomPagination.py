#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
@author: HighWay.Li
@contact:byamian@gmail.com
@version: 1.0.0
@license: Apache Licence
@file: CustomPagination.py
@time: 11/20/24 PM10:51
"""

from rest_framework.pagination import PageNumberPagination,LimitOffsetPagination
from rest_framework.response import Response

class MyLimitPagination(LimitOffsetPagination):
    default_limit = 10
    limit_query_param = 'limit'
    offset_query_param = 'offset'
    max_limit = 100

    def get_paginated_response(self, data):
        return Response({
            'count': self.count,
            'next': self.get_next_link(),
            'previous': self.get_previous_link(),
            'records': data
        })


class CustomPageNumberPagination(PageNumberPagination):
    page_size = 10  # 默认的每页记录数
    page_query_param = 'page_size'  # 客户单指定每页条数的参数名称
    max_page_size = 100 #  每页最大记录数

    class CustomPagination(
        PageNumberPagination): page_size = 10  # 默认每页显示的记录数 page_size_query_param = 'page_size' # 允许客户端在请求中指定每页条数 max_page_size = 100 # 每页最大记录数
    # 重写分页返回方法
    def get_paginated_response(self, data):
        return Response({
            "count": self.page.paginator.count,
            "next": self.get_next_link(),
            "previous": self.get_previous_link(),
            "records": data
        })