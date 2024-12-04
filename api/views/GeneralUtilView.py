#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
@author: HighWay.Li
@contact:byamian@gmail.com
@version: 1.0.0
@license: Apache Licence
@file: GeneralUtilView.py
@time: 12/4/24 PM6:30
"""
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet, ModelViewSet
from django.apps import apps

class GeneralUtilViewSet(ViewSet):

    """
    GET : localhost:8000/api/v1/getDropDown?table_name=CONFIG_INFO&column_name=config_name

    """
    def dropDown(self, request):
        table_name= request.query_params.get('table_name')
        column_name = request.query_params.get('column_name')
        if not table_name or not column_name:
            return Response({"error":'Table name and column name are required'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            model = apps.get_model(app_label='api',model_name=table_name)
            unique_values = model.objects.values_list(column_name, flat=True).distinct()
            return Response({'data':list(unique_values)}, status=status.HTTP_200_OK)
        except LookupError:
            return Response({'error':f'Model {table_name} not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error':str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

