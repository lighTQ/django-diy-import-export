#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
@author: HighWay.Li
@contact:byamian@gmail.com
@version: 1.0.0
@license: Apache Licence
@file: generic_view.py
@time: 11/17/24 PM7:51

1. 比API封装更高级一点 ，extends APIView

"""
from django.contrib.admin.utils import lookup_field
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView, ListCreateAPIView

from api.models import Person, PersonSerializer
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



# 2. 使用mixins 方法model进一步简化逻辑
from rest_framework.mixins import CreateModelMixin, UpdateModelMixin,ListModelMixin,RetrieveModelMixin,DestroyModelMixin


class BookGenericAPIView(GenericAPIView,ListModelMixin,CreateModelMixin):
    queryset = Books.objects.all()
    serializer_class = BooksModelSerializer
    def get(self, request, *args, **kwargs):

        return self.list(request, *args, **kwargs)
        # obj_list = self.get_queryset()
        # serializer = self.get_serializer(obj_list, many=True)
        # return Response(serializer.data)
        #

    def perform_create(self, serializer):
        # 加上自己的校验逻辑
        super().perform_create(serializer)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

        # ser = self.get_serializer(data= request.data)
        # if ser.is_valid():
        #     ser.save()
        # return Response(ser.data)


class BookDetailGenericAPIView(GenericAPIView,RetrieveModelMixin,DestroyModelMixin,UpdateModelMixin):
    queryset = Books.objects.all()
    serializer_class = BooksModelSerializer
    # 指定单条查询的字段, 跟url里的保持一致
    lookup_field = 'name'
    def get(self, request, name, *args, **kwargs):
        return self.retrieve(request, name, *args, **kwargs)

        # obj =self.get_object()
        # ser = self.get_serializer(obj)
        # return Response(ser.data)

    def perform_destroy(self, instance):

        # check logic
        super().destroy(instance)
    def delete(self, request, name, *args, **kwargs):

       return  self.destroy(request, name, *args, **kwargs)

        # obj = self.get_object()
        # obj.delete()
        # return Response({})

    def perform_update(self, serializer):
        # update logic
        super().update(serializer)


    def put(self, request, name, *args, **kwargs):
        return self.update(request, name, *args, **kwargs)
        # obj = self.get_object()
        # ser = self.get_serializer(obj,request.data)
        # if ser.is_valid():
        #     ser.save()
        #     return Response(ser.data)



## 第三层封装， 基于视图子类实现5个接口（9个）,实际中用哪个实现哪个， 在序列化类中实现局部钩子做校验
from rest_framework.generics import (ListCreateAPIView,CreateAPIView,RetrieveAPIView,
                                     DestroyAPIView,UpdateAPIView,ListCreateAPIView,
                                     RetrieveUpdateAPIView,DestroyAPIView,RetrieveUpdateDestroyAPIView)

class BookView2(ListCreateAPIView):
    queryset = Books.objects.all()
    serializer_class = BooksModelSerializer

class Book2DetailView(RetrieveUpdateDestroyAPIView):
    queryset = Books.objects.all()
    serializer_class = BooksModelSerializer
    lookup_field = 'name'


# 第四层封装，使用modelViewSet 做
from rest_framework.viewsets import ModelViewSet,ReadOnlyModelViewSet,GenericViewSet,ViewSet

class BookView3(ModelViewSet):
    queryset = Books.objects.all()
    serializer_class = BooksModelSerializer
    lookup_field = 'name'


class IndexView(ViewSet):
    objects_all = Person.objects.all()
    serializer = PersonSerializer(objects_all,many=True)
    lookup_field = 'name'
    # 自定义方法然后再url中进行绑定
    def lhw(self,request,name,*args,**kwargs):
        return Response({"msg":"hello world, hello :"+name})