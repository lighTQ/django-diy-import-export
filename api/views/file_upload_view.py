#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
@author: HighWay.Li
@contact:byamian@gmail.com
@version: 1.0.0
@license: Apache Licence
@file: file_upload_view.py
@time: 12/6/24 PM6:59
"""
import pandas as pd
from django.db.models import Max
from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet

from api.models.models import CONFIG_INFO, ConfigModelSerializer


class FileUploadView(ViewSet):

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