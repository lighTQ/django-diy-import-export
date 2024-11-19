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
from pandas.io.formats.style import buffering_args
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from datetime import datetime

from api.models import CONFIG_INFO, ConfigModelSerializer

class MyModelViewSet(ModelViewSet):

    # 重写某些方法
    def list(self, request, *args, **kwargs):
        response = super(MyModelViewSet, self).list(request, *args, **kwargs)
        res = {'result':response.data, 'msg':'查询成功', 'code':status.HTTP_200_OK}
        return Response(res)

class ConfigModelView(MyModelViewSet):
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

    """ 
    根据前台的boby参数更新数据库，并且生成excel文件流上传到sftp
    
    
    """
    @action(detail=False, methods=['post'])
    def filling(self,request, *args, **kwargs):
        try:
            pass
            # sftp=sftp_utilsV1("","","")
            # remote=sftpCfp.remote_toVsm_dir
            # client=sftp.get_sftp_client()
            print(request.data)
            data =request.data['data']
            df = pd.DataFrame([data])
            ts =datetime.now().strftime('%Y%m%d%H%M%S')
            config_no = data['config_no']
            opt_status = data['opt_status']
            # 更新数据
            CONFIG_INFO.objects.filter(id=config_no).update(opt_status=opt_status,last_update=datetime.now())
            filename = f'DG-{ts}-SHORT-CHECK-{config_no}.xlsx'
            # 创建BytesIO对象
            from io import BytesIO
            buffer = BytesIO()
            with pd.ExcelWriter(buffer, engine='openpyxl')  as writer:
                df.to_excel(writer, index=False,sheet_name='Sheet1')
            buffer.seek(0)

            # client.putfo(buffer,remote+filename)
            buffer.close()
            return Response({'msg':'200'}, status=status.HTTP_200_OK)

        except Exception as e:

            return Response(str(e), status=status.HTTP_400_BAD_REQUEST)


    """
    导入excel数据，生成dataframe，然后根据条件判断是再数据库中新增还是创建
    """
    @action(detail=False, methods=['post'])
    def importData(self,request, *args, **kwargs):
        try:
            file = request.data['file']
            df = pd.read_excel(file)
            print(df)
            for idx, row in df.iterrows():
                row_dict= row.to_dict()
                cfg_name = row_dict['cfg_name']
                cfg_category = row_dict['config_category']
                instance,created = CONFIG_INFO.objects.get_or_create(config_name=cfg_name,
                                                                     config_category=cfg_category, defaults=row_dict, )
                if created:
                    instance.save()
                else:
                    instance.config_value=row_dict['config_value']
                    instance.last_update=datetime.now()
                    instance.save(force_update=True)
            return Response({'msg':'200'}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(str(e), status=status.HTTP_400_BAD_REQUEST)


















