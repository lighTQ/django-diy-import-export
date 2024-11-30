#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
@author: HighWay.Li
@contact:byamian@gmail.com
@version: 1.0.0
@license: Apache Licence
@file: basic_view.py
@time: 11/30/24 PM6:56
"""
import json
from datetime import datetime
from django.utils import timezone

from django.core.paginator import Paginator
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from api.utils.CustomPagination import JavaPageNumberPagination


class BasicView(ModelViewSet):
    pagination_class = JavaPageNumberPagination

    "JavaStyle PageList Response "
    @action(detail=False, methods=['post'], url_path='findPagedList/(?P<page_index>\d+)/(?P<page_size>\d+)')
    def findPagedList(self, request, page_index, page_size,*args, **kwargs):
        try:
            parmas = json.loads(request.body)
            # queryset= self.get_queryset().filter(**parmas)
            queryset = self.filter_queryset_with_params(self.get_queryset(), parmas)
            paginator = Paginator(queryset,page_size)
            page = paginator.page(page_index)
            ser = self.get_serializer(page,many=True)
            pagination = self.pagination_class()
            pagination.page = page
            return pagination.get_paginated_response(ser.data)
        except Exception as e:
            return Response({"msg":str(e)}, status=status.HTTP_400_BAD_REQUEST)


    """
    自定义过滤body参数
    """
    def filter_queryset_with_params(self,qs,params):
        if params:
            for key,value in params.items():
                if value!="":

                    if key.endswith('_date'):
                        try:
                            date_value = datetime.strptime(value, '%Y-%m-%d').date()
                            qs = qs.filter(**{f'{key}__date':date_value})
                        except ValueError as e:
                            print(f"日期格式错误：{0}".format(e))
                    else:
                        qs = qs.filter(**{key:value})
        return qs