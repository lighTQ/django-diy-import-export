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
import pandas as pd
from django.db.models import Max
from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet, ModelViewSet
from django.apps import apps

from api.models.models import CONFIG_INFO, ConfigModelSerializer


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


    """
    use postmethod upload mulltifiles with other params
    """
    def uploadPics(self, request, *args, **kwargs):
        try:
            transport_no =request.data['transportNo']
            print(f"transportNo: {transport_no}")
            df_list= []
            errors = []
            for file in request.FILES.getlist('file'):
                file_name = file.name
                print(f'upload {file_name}')
                file_obj = file.read()
                df = pd.read_excel(file_obj)
                print(df)
                df_list.append(df)

                for index, row in df.iterrows():
                    row_dict= row.to_dict()
                    if 'id' not in row_dict or pd.isnull(row_dict['id']):
                        max_id=CONFIG_INFO.objects.aggregate(Max('id'))['id__max']
                        if max_id is None:
                            max_id=0
                        row_dict['id'] = max_id + 1
                    ser = ConfigModelSerializer(data=row.to_dict())
                    if ser.is_valid():
                        instance, created = CONFIG_INFO.objects.update_or_create(
                            id=row.get('id'),
                            defaults=row_dict,
                        )
                    else:
                        errors.append(ser.errors)
            merge_df = pd.concat(df_list)
            print(merge_df.count())
            print(merge_df.head())
            print(merge_df.tail())
            if errors:
                return Response(errors, status=status.HTTP_400_BAD_REQUEST)
            return Response(merge_df.to_dict(orient='records'), status=status.HTTP_200_OK)
        except Exception as e:
            return Response(str(e), status=status.HTTP_400_BAD_REQUEST)