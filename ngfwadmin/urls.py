from django.urls import path

from ngfwadmin.views.state.state import *
from ngfwadmin.views.ports.ports import *
from ngfwadmin.views.debug.error import *
from ngfwadmin.views.rules.rules import *
from ngfwadmin.views.rules.lists import *
from ngfwadmin.views.debug.table import *
from ngfwadmin.views.ipsids.ipsids import *
from ngfwadmin.views.rules.history import *
from ngfwadmin.views.protocols.nat import *
from ngfwadmin.views.protocols.arp import *
from ngfwadmin.views.protocols.dhcp import *
from ngfwadmin.views.protocols.route import *
from ngfwadmin.views.protocols.ipconfig import *
from ngfwadmin.views.inspection.inspection import *
from ngfwadmin.views.syslog.syslog import *

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

    # Система обнаружения вторжений
    path('ipsids/', ipsids, name='ipsids'),

    # Контентная фильтрация
    path('inspection/', inspection, name='inspection'),

    path('syslog/', syslog, name='syslog'),

    # Протоколы
    path('protocol/arp/', protocol_arp, name='protocol_arp'),
    path('protocol/dhcp/', protocol_dhcp, name='protocol_dhcp'),
    path('protocol/nat/', protocol_nat, name='protocol_nat'),
    path('protocol/nat/new/', protocol_nat_add, name='protocol_nat_add'),
    path('protocol/route/', protocol_route, name='protocol_route'),
    path('protocol/route/new', protocol_route_add, name='protocol_route_add'),
    path('protocol/ipconfig/', protocol_ipconfig, name='protocol_ipconfig'),
    path('protocol/ipconfig/new', protocol_ipconfig_add, name='protocol_ipconfig_add'),

    # Справочные таблицы
    path('rules/table/<slug:name>/', table, name='table'),

    # Отображение ошибок
    path('error/', error, name='error'),
]
