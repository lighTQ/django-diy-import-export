#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
@author: HighWay.Li
@contact:byamian@gmail.com
@version: 1.0.0
@license: Apache Licence
@file: config_view.py
@time: 11/18/24 PM8:38
"""
import uuid

import pandas as pd
from django.core.serializers import serialize
from django.db.models import Max
from django.http import HttpResponse
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from api.models import CONFIG_INFO, ConfigModelSerializer


class ConfigModelView(ModelViewSet):
    queryset = CONFIG_INFO.objects.all()
    serializer_class = ConfigModelSerializer

    filter_backends = (DjangoFilterBackend,)
    filterset_fields = "__all__"
    # ordering_fields = "__all__"
    ordering_fields = ['id','config_name']

    @action(detail=False, methods=['get'])
    def export(self, request, *args, **kwargs):
        try:
            print(request.query_params)
            qs = self.filter_queryset(self.get_queryset())
            data = list(qs.values())
            ser = ConfigModelSerializer(data=data, many=True)
            if ser.is_valid():
                # data transform
                df = pd.DataFrame(ser.data)
                print(df)
                response = HttpResponse(content_type='application/ms-excel')
                response['Content-Disposition'] = 'attachment; filename="config_info_exported.xlsx"'
                with pd.ExcelWriter(response, engine='xlsxwriter') as writer:
                    df.to_excel(writer, index=False,sheet_name='Sheet1')
                    return response
            else:
                return Response(ser.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response(str(e), status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['post'])
    def upload(self, request, *args, **kwargs):
        try:
            file = request.data['file']
            df = pd.read_excel(file)
            print(df)
            errors=[]
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
            if errors:
                return Response(errors, status=status.HTTP_400_BAD_REQUEST)
            return Response(df.to_dict(orient='records'), status=status.HTTP_200_OK)
        except Exception as e:
            return Response(str(e), status=status.HTTP_400_BAD_REQUEST)

