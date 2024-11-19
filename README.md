使用drf 框架的apiview 完成excel的自定义import和export 功能

1. 实现通过postmanform表单提交文件和参数到后台，然后后台解析参数和文件，入库
2. 实现通过postman 接受body的参数，作为查询条件，校验过滤后台数据，然后导出excel
3. api doc 《https://www.cnblogs.com/tully/p/16979367.html》
要在Django REST Framework (DRF)中配置Swagger生成接口文档，可以按照以下步骤进行：

安装所需的包：

sh
`
pip install djangorestframework
pip install drf-yasg
`
在settings.py中配置INSTALLED_APPS：

python
`
INSTALLED_APPS = [
    ...
    'rest_framework',
    'drf_yasg',
    ...
]
`
在urls.py中配置Swagger和Schema视图：

python
`
from django.urls import path, include
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions

schema_view = get_schema_view(
    openapi.Info(
        title="API Documentation",
        default_version='v1',
        description="API documentation for my project",
        terms_of_service="https://www.google.com/",
        contact=openapi.Contact(email="contact@myproject.com"),
        license=openapi.License(name="Apache License 2.0"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    ...
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    ...
]
`
确保你的模板中包含Swagger UI： 在你的HTML模板中，添加以下代码来加载Swagger UI：

html
<!DOCTYPE html>
<html>
<head>
    <title>Swagger UI</title>
    <link rel="stylesheet" type="text/css" href="https://unpkg.com/swagger-ui-dist@3/swagger-ui.css" />
</head>
<body>
    <div id="swagger-ui"></div>
    <script src="https://unpkg.com/swagger-ui-dist@3/swagger-ui-bundle.js"></script>
    <script>
        const ui = SwaggerUIBundle({
            url: '{% url 'schema-swagger-ui' %}',
            dom_id: '#swagger-ui',
            presets: [
                SwaggerUIBundle.presets.apis,
                SwaggerUIBundle.SwaggerUIStandalonePreset
            ],
            layout: "BaseLayout",
            requestInterceptor: (req) => {
                req.headers['X-CSRFToken'] = '{{ csrf_token }}';
                return req;
            }
        });
    </script>
</body>
</html>
