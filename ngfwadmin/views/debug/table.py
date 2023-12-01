from ngfwadmin.rest.sys.sys import sys_ports_get, settings_get
from ngfwadmin.rest.rules.enum import *
from ngfwadmin.rest.ports.ports import *
from ngfwadmin.views.connect.connect import *
from ngfwadmin.rest.monitoring.monitoring import *

from django.shortcuts import redirect, render


# Страница таблиц Debug
def table(request, name):
    try:
        # Подключение
        dev = get_connect()

        # Проверка подключения
        if 'url' not in dev:
            return redirect('connect')

        # параметры таблицы
        rows = []
        columns = []
        caption = ''

        if name == 'atomic':
            caption = 'atomic'
            atomic = enum_atomic_get(dev.get('url'))
            columns = ['id', 'file_type', 'description', 'rule_category', 'arg_type']
            for i in atomic:
                row = atomic[i]
                id = row['id']
                arg_type = row.get('arg_type')
                file_type = row.get('file_type')
                description = row.get('description')
                rule_category = row.get('rule_category')
                rows.append([id, file_type, description, rule_category, arg_type])

        elif name == 'format':
            caption = 'formats'
            formats = enum_format_get(dev.get('url'))
            columns = ['id', 'name', 'print', 'description', 'param']
            for row in formats['formats']:
                id = row.get('id')
                name = row.get('name')
                print = row.get('print')
                param = row.get('param')
                description = row.get('description')
                rows.append([id, name, print, description, param])

        elif name == 'services':
            caption = 'services'
            services = enum_services_get(dev.get('url'))
            columns = ['services']
            for val in services:
                rows.append([val])

        elif name == 'protocols':
            caption = 'protocols'
            protocols = enum_protocols_get(dev.get('url'))
            columns = ['protocols']
            for val in protocols:
                rows.append([val])

        elif name == 'ports':
            caption = 'ports'
            ports = ports_get(dev.get('url'))
            columns = ['link_status', 'rx_nombuf', 'link_speed', 'ibytes', 'obytes', 'number', 'oerrors', 'imissed',
                       'ibits_per_sec', 'ipackets', 'imissed_per_sec', 'opackets_per_sec', 'link_duplex',
                       'ipackets_per_sec', 'driver_name', 'opackets', 'ierrors', 'obits_per_sec']
            for val in ports:
                ibytes = val.get('ibytes')
                obytes = val.get('obytes')
                number = val.get('number')
                oerrors = val.get('oerrors')
                imissed = val.get('imissed')
                ierrors = val.get('ierrors')
                ipackets = val.get('ipackets')
                opackets = val.get('opackets')
                rx_nombuf = val.get('rx_nombuf')
                link_speed = val.get('link_speed')
                link_status = val.get('link_status')
                link_duplex = val.get('link_duplex')
                driver_name = val.get('driver_name')
                ibits_per_sec = val.get('ibits_per_sec')
                obits_per_sec = val.get('obits_per_sec')
                imissed_per_sec = val.get('imissed_per_sec')
                opackets_per_sec = val.get('opackets_per_sec')
                ipackets_per_sec = val.get('ipackets_per_sec')
                rows.append(
                    [link_status, rx_nombuf, link_speed, ibytes, obytes, number, oerrors, imissed, ibits_per_sec,
                     ipackets, imissed_per_sec, opackets_per_sec, link_duplex, ipackets_per_sec, driver_name, opackets,
                     ierrors, obits_per_sec])

        elif name == 'ports_avail':
            caption = 'ports_avail'
            ports = ports_avail_get(dev.get('url'))
            columns = ['driver_name', 'duplex', 'numa', 'speed', 'status']
            for val in ports:
                numa = val.get('numa')
                speed = val.get('speed')
                status = val.get('status')
                duplex = val.get('duplex')
                driver_name = val.get('driver_name')
                rows.append([driver_name, duplex, numa, speed, status])

        elif name == 'system_ports':
            caption = 'system_ports'
            ports = sys_ports_get(dev.get('url'))
            columns = ['rss_type','tx_ring_size','rx_ring_size','port_number','wan','packet_max_len','name','enable','icmp_disable','dhcp','mac','description','ipconfig']
            for val in ports:
                wan = val.get('wan')
                mac = val.get('mac')
                name = val.get('name')
                dhcp = val.get('dhcp')
                enable = val.get('enable')
                ipconfig = val.get('ipconfig')
                rss_type = val.get('rss_type')
                description = val.get('description')
                port_number = val.get('port_number')
                icmp_disable = val.get('icmp_disable')
                tx_ring_size = val.get('tx_ring_size')
                rx_ring_size = val.get('rx_ring_size')
                packet_max_len = val.get('packet_max_len')
                rows.append([rss_type,tx_ring_size,rx_ring_size,port_number,wan,packet_max_len,name,enable,icmp_disable,dhcp,mac,description,ipconfig])

        elif name == 'system_settings':
            caption = 'system_settings'
            settings = settings_get(dev.get('url'))
            columns = ['name','title','element','type','visible','default','min','max','description']
            for val in settings.get('parameters'):
                min = val.get('min')
                max = val.get('max')
                name = val.get('name')
                type = val.get('type')
                title = val.get('title')
                element = val.get('element')
                visible = val.get('visible')
                default = val.get('default')
                description = val.get('description')
                rows.append([name,title,element,type,visible,default,min,max,description])

        # отобразить страницу с таблицей
        context = {'dev': dev,
                   'name': name,
                   'rows': rows,
                   'caption': caption,
                   'columns': columns, }
        return render(request, 'debug/table.html', context=context)

    # обработка ошибок
    except Exception as ex:
        return exception(request, ex)
