# from django.contrib.auth.models import UserManager
# from django.db import models

#
# # Устройства NGFW
# class Device(models.Model):
#     name = models.CharField(max_length=1024, verbose_name='Название')
#     ip = models.CharField(max_length=255, verbose_name='IP адрес')
#     port = models.CharField(max_length=255, verbose_name='Порт')
#     login = models.CharField(max_length=255, verbose_name='Логин')
#     password = models.CharField(max_length=255, verbose_name='Пароль')
#     description = models.TextField(blank=True, verbose_name='Описание')
#     objects = UserManager()
#     # Мета класс для админки
#     class Meta:
#         verbose_name = 'Устройство NGFW'
#         verbose_name_plural = 'Устройства NGFW'
#         ordering = ['name']
