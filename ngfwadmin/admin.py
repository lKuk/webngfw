from django.contrib import admin

# Register your models here.
from .models import *


# # Класс отображения модели устройств в Admin панели
# class DeviceAdmin(admin.ModelAdmin):
#     list_display = ('id', 'name', 'ip', 'port', 'login', 'password')
#     search_fields = ('name', 'ip')
#
#
# # регистрация модели устройств в Admin панели
# admin.site.register(Device, DeviceAdmin)
