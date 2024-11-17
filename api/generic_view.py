#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
@author: HighWay.Li
@contact:byamian@gmail.com
@version: 1.0.0
@license: Apache Licence
@file: generic_view.py
@time: 11/17/24 PM7:51
比API封装更高级一点 ，extends APIView

"""
from django.contrib.admin.utils import lookup_field
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView

from api.serializer import PublishSerializer, PublishModelSerializer,BooksModelSerializer
from goods.models import Publish,Books


class PublishGenericAPIView(GenericAPIView):
    queryset = Publish.objects.all()
    serializer_class = PublishModelSerializer
    def get(self, request, *args, **kwargs):
        obj_list = self.get_queryset()
        serializer = self.get_serializer(obj_list, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        ser = self.get_serializer(data= request.data)
        if ser.is_valid():
            ser.save()
        return Response(ser.data)

class PublishDetailGenericAPIView(GenericAPIView):
    queryset = Publish.objects.all()
    serializer_class = PublishModelSerializer
    # 指定单条查询的字段, 跟url里的保持一致
    lookup_field = 'name'
    def get(self, request, name, *args, **kwargs):
        obj =self.get_object()
        ser = self.get_serializer(obj)
        return Response(ser.data)

    def post(self, request, name,*args, **kwargs):
        obj = self.get_object()
        ser = self.get_serializer(obj)
        if ser.is_valid():
            ser.save()
            return Response(ser.data)

    def delete(self, request, name, *args, **kwargs):
        obj = self.get_object()
        obj.delete()
        return Response({})

    def put(self, request, name, *args, **kwargs):
        obj = self.get_object()
        ser = self.get_serializer(obj,request.data)
        if ser.is_valid():
            ser.save()
            return Response(ser.data)





class BookGenericAPIView(GenericAPIView):
    queryset = Books.objects.all()
    serializer_class = BooksModelSerializer
    def get(self, request, *args, **kwargs):
        obj_list = self.get_queryset()
        serializer = self.get_serializer(obj_list, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        ser = self.get_serializer(data= request.data)
        if ser.is_valid():
            ser.save()
        return Response(ser.data)

class BookDetailGenericAPIView(GenericAPIView):
    queryset = Books.objects.all()
    serializer_class = BooksModelSerializer
    # 指定单条查询的字段, 跟url里的保持一致
    lookup_field = 'name'
    def get(self, request, name, *args, **kwargs):
        obj =self.get_object()
        ser = self.get_serializer(obj)
        return Response(ser.data)

    def post(self, request, name,*args, **kwargs):
        obj = self.get_object()
        ser = self.get_serializer(obj)
        if ser.is_valid():
            ser.save()
            return Response(ser.data)

    def delete(self, request, name, *args, **kwargs):
        obj = self.get_object()
        obj.delete()
        return Response({})

    def put(self, request, name, *args, **kwargs):
        obj = self.get_object()
        ser = self.get_serializer(obj,request.data)
        if ser.is_valid():
            ser.save()
            return Response(ser.data)


from rest_framework.mixins import CreateModelMixin, UpdateModelMixin,ListModelMixin,RetrieveModelMixin,DestroyModelMixin

from rest_framework.viewsets import ModelViewSet



