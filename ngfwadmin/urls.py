from django.urls import path

from ngfwadmin.views.auth.auth import auth, auth_user
from ngfwadmin.views.auth.permissions import permissions
from ngfwadmin.views.debug.error import error
from ngfwadmin.views.debug.table import table
from ngfwadmin.views.ports.ports import ports
from ngfwadmin.views.state.state import state
from ngfwadmin.views.write.write import write, write_download
from ngfwadmin.views.ipsids.ipsids import ipsids
from ngfwadmin.views.syslog.syslog import syslog
from ngfwadmin.views.rules.history import history
from ngfwadmin.views.protect.protect import protect
from ngfwadmin.views.connect.connect import connect, welcome
from ngfwadmin.views.protocols.arp import protocol_arp
from ngfwadmin.views.inspection.inspection import inspection
from ngfwadmin.views.protocols.dhcp import protocol_dhcp_table
from ngfwadmin.views.rules.lists import lists, lists_add, lists_edit
from ngfwadmin.views.classification.classification import classification
from ngfwadmin.views.protocols.nat import protocol_nat, protocol_nat_add
from ngfwadmin.views.protocols.route import protocol_route, protocol_route_add
from ngfwadmin.views.rules.rules import rules, rules_add, rules_edit, rules_sub_edit
from ngfwadmin.views.protocols.ipconfig import protocol_ipconfig, protocol_ipconfig_add
from ngfwadmin.views.protocols.dhcp import protocol_dhcp_subnet_edit, protocol_dhcp_subnet
from ngfwadmin.views.protocols.dhcp import protocol_dhcp_static, protocol_dhcp_static_add
from ngfwadmin.views.service.ping import ping
from ngfwadmin.views.service.ldap import ldap, user_add
from ngfwadmin.views.service.ntp import ntp, client_add

urlpatterns = [
    # Форма подключения к устройству
    path('connect/', connect, name='connect'),
    path('welcome/', welcome, name='welcome'),

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

    # Классификаторы
    path('classification/', classification, name='classification'),

    # Системный журнал
    path('syslog/', syslog, name='syslog'),

    # Защита сети
    path('protect/', protect, name='protect'),

    # Аутентификация
    path('auth/', auth, name='auth'),
    path('permissions/', permissions, name='permissions'),
    path('auth/user/<str:user>', auth_user, name='auth_user'),

    # Запись трафика
    path('write/', write, name='write'),
    path('write/download/<str:name>', write_download, name='write_download'),

    # Протоколы
    path('protocol/arp/', protocol_arp, name='protocol_arp'),
    path('protocol/nat/', protocol_nat, name='protocol_nat'),
    path('protocol/route/', protocol_route, name='protocol_route'),
    path('protocol/nat/new/', protocol_nat_add, name='protocol_nat_add'),
    path('protocol/ipconfig/', protocol_ipconfig, name='protocol_ipconfig'),
    path('protocol/route/new/', protocol_route_add, name='protocol_route_add'),
    path('protocol/dhcp/table/', protocol_dhcp_table, name='protocol_dhcp_table'),
    path('protocol/dhcp/subnet/', protocol_dhcp_subnet, name='protocol_dhcp_subnet'),
    path('protocol/dhcp/static/', protocol_dhcp_static, name='protocol_dhcp_static'),
    path('protocol/ipconfig/new/', protocol_ipconfig_add, name='protocol_ipconfig_add'),
    path('protocol/dhcp/static/new/', protocol_dhcp_static_add, name='protocol_dhcp_static_add'),
    path('protocol/dhcp/subnet/<int:port>/<int:vlan>', protocol_dhcp_subnet_edit, name='protocol_dhcp_subnet_edit'),

    # Сервис
    path('service/ping', ping, name='ping'),
    path('service/ldap', ldap, name='ldap'),
    path('service/ldap/new', user_add, name='ldap_add'),
    path('service/ntp', ntp, name='ntp'),
    path('service/ntp/new', client_add, name='ntp_add'),


    # Справочные таблицы
    path('table/<slug:name>/', table, name='table'),

    # Отображение ошибок
    path('error/', error, name='error'),
]
