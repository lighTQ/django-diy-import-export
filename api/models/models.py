#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
@author: HighWay.Li
@contact:byamian@gmail.com
@version: 1.0.0
@license: Apache Licence
@file: models.py
@time: 11/17/24 PM2:40
"""
from django.db import models
from rest_framework import serializers

class Person(models.Model):
    name = models.CharField(max_length=100)
    age = models.IntegerField()
    sex = models.CharField(max_length=100)

class PersonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Person
        fields ='__all__'

    def isvalid(self):
        return self.is_valid

    def create(self, validated_data):
        return Person.objects.create(**validated_data)

class CONFIG_INFO(models.Model):
    id = models.AutoField(primary_key=True)
    config_category=models.CharField(max_length=100)
    config_name = models.CharField(max_length=100)
    config_value = models.CharField(max_length=100)
    config_remark = models.CharField(max_length=100)
    create_date = models.DateTimeField(auto_created=True)
    last_update = models.DateTimeField(auto_now=True)

class ConfigModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = CONFIG_INFO
        fields ='__all__'
        extra_kwargs = {'create_date': {'required': False}}