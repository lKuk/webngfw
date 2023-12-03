from django.urls import path

from ngfwadmin.views.sys.sys import *
from ngfwadmin.views.ports.ports import *
from ngfwadmin.views.debug.error import *
from ngfwadmin.views.rules.rules import *
from ngfwadmin.views.rules.lists import *
from ngfwadmin.views.debug.table import *
from ngfwadmin.views.rules.history import *

urlpatterns = [
    # Форма подключения к устройству
    path('connect/', connect, name='connect'),

    # По умолчанию
    path('', sys, name='sys'),

    # Система
    path('sys/', sys, name='sys'),
    path('sys_ajax/', sys_ajax, name='sys_ajax'),

    # Порты
    path('ports/', ports, name='ports'),
    path('ports_ajax/', ports_ajax, name='ports_ajax'),

    # Редактор правила
    path('rules/', rules, name='rules'),
    path('rules/new/', rules_add, name='rules_add'),
    path('rules/<int:id>/', rules_edit, name='rules_edit'),
    path('rules/<int:id>/sub', rules_sub_edit, name='rules_sub_edit'),

    # Редактор списков
    path('rules/lists/', lists, name='lists'),
    path('rules/lists/new/', lists_add, name='lists_add'),
    path('rules/lists/<int:id>/', lists_edit, name='lists_edit'),

    # История изменений
    path('rules/history/', history, name='history'),

    # Справочные таблицы
    path('rules/table/<slug:name>/', table, name='table'),

    # Отображение ошибок
    path('error/', error, name='error'),
]
