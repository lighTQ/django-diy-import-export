"""
URL configuration for core project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework.documentation import include_docs_urls

from api.views.homeView import HomePageView

# router = SimpleRouter()
# router.register('book', views.BookView)
# print(router.urls)


from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions
schema_view = get_schema_view( openapi.Info( title="API Documentation",
                                default_version='v1',
                                description="API documentation for my project",
                                terms_of_service="https://www.google.com/",
                                contact=openapi.Contact(email="contact@myproject.com"),
                                license=openapi.License(name="Apache License 2.0"), ),
                               public=True,
                                permission_classes=[permissions.AllowAny,], )


urlpatterns = [
               path('',HomePageView.as_view(),name='homePage') ,
               path('admin/', admin.site.urls),
               path('api/v1/', include('api.urls'),name='api'),
               path('study/v1/',include('goods.urls'),name='study'),
               path('docs/', include_docs_urls(title='我的coreapi 接口文档')),
               path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
               path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),                ]
# urlpatterns += router.urls
print('core \n')
print(urlpatterns)

