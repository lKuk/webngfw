from django.urls import path

from ngfwadmin.views.rules.rules import *
from ngfwadmin.views.rules.lists import *
from ngfwadmin.views.debug.table import *
from ngfwadmin.views.rules.history import *
from ngfwadmin.views.system.system import *

urlpatterns = [
    # Форма подключения к устройству
    path('connect/', connect, name='connect'),

    # Dashboard
    path('', system, name='system'),
    path('system/', system, name='system'),

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
