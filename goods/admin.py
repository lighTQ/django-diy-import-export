from django.contrib import admin
#
import api.models
# Register your models here.
#
from . import models
admin.site.register(models.Goods)
admin.site.register(models.Publish)
admin.site.register(models.Books)
# admin.site.register(api.models.Person)
# admin.site.register(api.models.CONFIG_INFO)