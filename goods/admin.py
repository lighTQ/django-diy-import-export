from django.contrib import admin
#
# Register your models here.
#
from . import models
admin.site.register(models.Goods)
admin.site.register(models.Publish)
admin.site.register(models.Books)