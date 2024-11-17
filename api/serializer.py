#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
@author: HighWay.Li
@contact:byamian@gmail.com
@version: 1.0.0
@license: Apache Licence
@file: serializer.py
@time: 11/15/24 PM7:16
"""
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from goods.models import Goods, Publish, Books


class GoodsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Goods
        fields = '__all__'


# class PublishSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Publish
#         fields = '__all__'



class BooksModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Books
        fields = '__all__'


class BooksSerializer(serializers.Serializer):
    # 字段跟原名称绑定
    # book_name = serializers.CharField(max_length=100,source='name')
    # 字段跟方法绑定
    id= serializers.IntegerField()
    book_name = serializers.CharField(max_length=100,source='get_book_name')
    price = serializers.IntegerField()
    # publish = serializers.CharField(source='publish_detail')ter
    # publish_detail = serializers.CharField()
    publish = serializers.SerializerMethodField()
    def get_publish(self, obj):
        return {'name':obj.publish.name,'addr':obj.publish.addr}

    # 如果要更新一定要重写update防风
    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.price = validated_data.get('price', instance.price)
        instance.publish = validated_data.get('publish', instance.publish)
        # 保存
        instance.save()
        # 返回
        return instance

    def create(self, validated_data):
        return Books.objects.create(**validated_data)



class PublishSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=100,min_length=3)
    # 序列化的名称的必须和前台请求的参数保持一致，要么就用model里面的字段， 要么就前台要用serializer映射之后的字段
    address = serializers.CharField(max_length=100,min_length=3,source='addr')
    # addr = serializers.CharField(max_length=100,min_length=3)

# 局部钩子，先走所有的局部钩子，都通过之后，然后再走全局的
    def validate_name(self, name):
        if name.startswith('sb'):
            raise ValidationError("wtf! ,name不能以sb开头")
        else:
            return name

# 全局钩子校验
    # def validate(self, attrs):
    #     name = attrs.get('name')
    #     address = attrs.get('address')
    #     price = attrs.get('price')
    #     print({'name':name,'address':address,'price':price})
    #     return attrs

    def create(self, validated_data):
        return Publish.objects.create(**validated_data)


class PublishModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Publish
        fields = '__all__'
        # fields=['id','name']  # 部分字段序列化

