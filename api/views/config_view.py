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
import json

import pandas as pd
from django.http import HttpResponse
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from datetime import datetime
from rest_framework.renderers import TemplateHTMLRenderer
from api.models.models import CONFIG_INFO, ConfigModelSerializer
from api.views.basic_view import BasicView



class ConfigModelView(BasicView):
    queryset = CONFIG_INFO.objects.all()
    serializer_class = ConfigModelSerializer

    filter_backends = (DjangoFilterBackend,)
    filterset_fields = "__all__"
    # ordering_fields = "__all__"
    ordering_fields = ['id','config_name']
    # renderer_classes = (TemplateHTMLRenderer,)
    # template_name = 'config_info.html'

    def list(self, request, *args, **kwargs):
        self.renderer_classes = (TemplateHTMLRenderer,)
        self.template_name = 'config_info.html'
        queryset = self.filter_queryset(self.get_queryset())
        paginator = self.pagination_class()
        # 确保传递了request参数
        page = paginator.paginate_queryset(queryset, request)
        if page is not None:
            serializer = self.serializer_class(page, many=True)
            print(serializer.data)
            return paginator.get_paginated_response(serializer.data)
        serializer = self.serializer_class(queryset, many=True)
        return Response({"records": serializer.data}, status=status.HTTP_200_OK)




    @action(detail=False, methods=['post'])
    def export(self, request, *args, **kwargs):
        try:
            params= json.loads(request.body)
            print(params)
            # qs = self.get_queryset().filter(**params)
            qs=self.filter_queryset_with_params(self.get_queryset(),params)
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




    """ 
    根据前台的boby参数更新数据库，并且生成excel文件流上传到sftp
    """
    @action(detail=False, methods=['post'])
    def filling(self,request, *args, **kwargs):
        try:
            pass
            # sftp=sftp_utilsV1("","","")
            # remote=sftpCfp.remote_toZkpk_dir
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


















