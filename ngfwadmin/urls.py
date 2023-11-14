from .views import *
from django.urls import path

urlpatterns = [
    # Форма подключения к устройству
    path('device/', device, name='device'),

    # Dashboard
    path('', dashboard, name='dashboard'),

    # Редактор правила
    path('rules/', rules, name='rules'),
    path('rules/lists/', lists, name='lists'),
    path('rules/history/', history, name='history'),
    path('rules/<int:id>/', subrules, name='subrules'),
    path('rules/lists/<int:id>/content/', content, name='content'),


    # Справочные таблицы
    path('rules/table/<slug:name>/', table, name='table'),
]

