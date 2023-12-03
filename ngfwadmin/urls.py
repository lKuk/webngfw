from django.urls import path

from ngfwadmin.views.state.state import *
from ngfwadmin.views.ports.ports import *
from ngfwadmin.views.debug.error import *
from ngfwadmin.views.rules.rules import *
from ngfwadmin.views.rules.lists import *
from ngfwadmin.views.debug.table import *
from ngfwadmin.views.rules.history import *
from ngfwadmin.views.protocols.protocols import *

urlpatterns = [
    # Форма подключения к устройству
    path('connect/', connect, name='connect'),

    # По умолчанию
    path('', state, name='state'),

    # Система
    path('state/', state, name='state'),

    # Порты
    path('ports/', ports, name='ports'),

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

    # Протоколы
    path('protocol/arp/', protocol_arp, name='protocol_arp'),
    path('protocol/nat/', protocol_nat, name='protocol_nat'),
    path('protocol/icmp/', protocol_icmp, name='protocol_icmp'),
    path('protocol/dhcp/', protocol_dhcp, name='protocol_dhcp'),
    path('protocol/ip_route/', protocol_ip_route, name='protocol_ip_route'),
    path('protocol/ip_route/new', protocol_ip_route_add, name='protocol_ip_route_add'),
    path('protocol/ip_config/', protocol_ip_config, name='protocol_ip_config'),

    # Справочные таблицы
    path('rules/table/<slug:name>/', table, name='table'),

    # Отображение ошибок
    path('error/', error, name='error'),
]
