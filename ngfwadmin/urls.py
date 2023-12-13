from django.urls import path

from ngfwadmin.views.debug.error import error
from ngfwadmin.views.debug.table import table
from ngfwadmin.views.ports.ports import ports
from ngfwadmin.views.state.state import state
from ngfwadmin.views.write.write import write
from ngfwadmin.views.ipsids.ipsids import ipsids
from ngfwadmin.views.syslog.syslog import syslog
from ngfwadmin.views.rules.history import history
from ngfwadmin.views.protect.protect import protect
from ngfwadmin.views.connect.connect import connect
from ngfwadmin.views.protocols.arp import protocol_arp
from ngfwadmin.views.inspection.inspection import inspection
from ngfwadmin.views.rules.lists import lists, lists_add, lists_edit
from ngfwadmin.views.protocols.nat import protocol_nat, protocol_nat_add
from ngfwadmin.views.protocols.route import protocol_route, protocol_route_add
from ngfwadmin.views.rules.rules import rules, rules_add, rules_edit, rules_sub_edit
from ngfwadmin.views.protocols.ipconfig import protocol_ipconfig, protocol_ipconfig_add
from ngfwadmin.views.protocols.dhcp import protocol_dhcp_table, protocol_dhcp_subnet, protocol_dhcp_static


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

    #Системный журнал
    path('syslog/', syslog, name='syslog'),

    #Защита сети
    path('protect/', protect, name='protect'),

    #Запись трафика
    path('write/', write, name='write'),

    # Протоколы
    path('protocol/arp/', protocol_arp, name='protocol_arp'),
    path('protocol/nat/', protocol_nat, name='protocol_nat'),
    path('protocol/nat/new/', protocol_nat_add, name='protocol_nat_add'),
    path('protocol/route/', protocol_route, name='protocol_route'),
    path('protocol/route/new', protocol_route_add, name='protocol_route_add'),
    path('protocol/ipconfig/', protocol_ipconfig, name='protocol_ipconfig'),
    path('protocol/ipconfig/new', protocol_ipconfig_add, name='protocol_ipconfig_add'),
    path('protocol/dhcp/table/', protocol_dhcp_table, name='protocol_dhcp_table'),
    path('protocol/dhcp/subnet/', protocol_dhcp_subnet, name='protocol_dhcp_subnet'),
    path('protocol/dhcp/static/', protocol_dhcp_static, name='protocol_dhcp_static'),

    # Справочные таблицы
    path('rules/table/<slug:name>/', table, name='table'),

    # Отображение ошибок
    path('error/', error, name='error'),
]
