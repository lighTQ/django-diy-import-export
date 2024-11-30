#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
@author: HighWay.Li
@contact:byamian@gmail.com
@version: 1.0.0
@license: Apache Licence
@file: diy_learn_view.py
@time: 11/30/24 PM7:00
"""
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response

from api.views.basic_view import BasicView


class MyModelViewSet(BasicView):

    # 重写某些方法
    def list(self, request, *args, **kwargs):
        print(self.action) #表示执行的是哪个方法
        response = super(MyModelViewSet, self).list(request, *args, **kwargs)
        res = {'result':response.data, 'msg':'查询成功', 'code':status.HTTP_200_OK}
        return Response(res)

    # 自己扩展的methods:派生
    @action(detail=False, methods=['get'], url_path='method_name_in_url_path, default=method_name')
    def login(self,request):
        return Response('登陆成功')

    @action(detail=True, methods=['get'])
    def login2(self,request,*args,**kwargs):
        # 获取生成pk路径的pk参数
        print(**kwargs)
        return Response('登陆成功')