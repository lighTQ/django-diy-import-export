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