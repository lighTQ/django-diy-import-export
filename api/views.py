#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
@author: HighWay.Li
@contact:byamian@gmail.com
@version: 1.0.0
@license: Apache Licence
@file: views.py
@time: 11/15/24 PM7:02
"""
from http.client import responses

from django.http import HttpResponse
from rest_framework import status, viewsets
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.viewsets import GenericViewSet, ModelViewSet

from api.serializer import GoodsSerializer, PublishSerializer
from goods.models import Goods, Publish
from rest_framework.views import View


@api_view(['GET'])
def get_data0(request):
    goods = {"name":"测试商品", "price":100.0}
    return Response(data=goods)

@api_view(['GET','POST'])
def goods_list(request):
    if request.method == 'GET':
        goods = Goods.objects.all()
        serializer = GoodsSerializer(goods, many=True)
        return Response(data=serializer.data)
    if request.method == 'POST':
        serializer = GoodsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)

@api_view(['GET','PUT','DELETE'])
def goods_detail(request,id):
    try:
        goods = Goods.objects.get(id=id)
    except Goods.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = GoodsSerializer(goods)
        return Response(data=serializer.data)
    if request.method == 'PUT':
        serializer = GoodsSerializer(goods, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    if request.method == 'DELETE':
        goods.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class PublishViewSet(ModelViewSet):
    queryset = Publish.objects.all()
    serializer_class = PublishSerializer

## CBV 源码执行流程
class Book(View):

    def dispatch(self, request, *args, **kwargs):
        # add code

        responses=super().dispatch(request, *args, **kwargs)
        return responses

    def get(self, request, *args, **kwargs):
        return HttpResponse('get response')

    def post(self, request, *args, **kwargs):
        return HttpResponse('post response')


from rest_framework.views import APIView
from rest_framework.response import Response

class BookAPIView(APIView):
    def get(self, request, *args, **kwargs):
        return Response("APIView Response")