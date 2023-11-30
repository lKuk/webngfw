
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

        # Атомарные правила
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

        # Формат атомарных правил
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

        # Список сервисов
        elif name == 'services':
            caption = 'services'
            services = enum_services_get(dev.get('url'))
            columns = ['services']
            for val in services:
                rows.append([val])

        # Список протоколов
        elif name == 'protocols':
            caption = 'protocols'
            protocols = enum_protocols_get(dev.get('url'))
            columns = ['protocols']
            for val in protocols:
                rows.append([val])

        elif name == 'monitoring_ram':
            caption = 'monitoring_ram'
            monitoring_ram = monitoring_ram_get(dev.get('url'))
            columns = ['percent', 'total', 'used']
            percent = monitoring_ram.get('percent')
            total = monitoring_ram.get('total')
            used = monitoring_ram.get('used')
            rows.append([percent, total, used])

        elif name == 'monitoring_disk':
            caption = 'monitoring_disk'
            monitoring_disk = monitoring_disk_get(dev.get('url'))
            columns = ['percent', 'total', 'used']
            percent = monitoring_disk.get('percent')
            total = monitoring_disk.get('total')
            used = monitoring_disk.get('used')
            rows.append([percent, total, used])

        elif name == 'monitoring_lcores':
            caption = 'monitoring_lcores'
            monitoring_lcores = monitoring_lcores_get(dev.get('url'))
            columns = ['val']
            for val in monitoring_lcores:
                rows.append([val])

        elif name == 'ports':
            caption = 'ports'
            ports = ports_get(dev.get('url'))
            columns = ['link_status', 'rx_nombuf', 'link_speed', 'ibytes', 'obytes', 'number', 'oerrors', 'imissed',
                       'ibits_per_sec', 'ipackets', 'imissed_per_sec', 'opackets_per_sec', 'link_duplex',
                       'ipackets_per_sec', 'driver_name', 'opackets', 'ierrors', 'obits_per_sec']
            for val in ports:
                link_status = val.get('link_status')
                rx_nombuf = val.get('rx_nombuf')
                link_speed = val.get('link_speed')
                ibytes = val.get('ibytes')
                obytes = val.get('obytes')
                number = val.get('number')
                oerrors = val.get('oerrors')
                imissed = val.get('imissed')
                ibits_per_sec = val.get('ibits_per_sec')
                ipackets = val.get('ipackets')
                imissed_per_sec = val.get('imissed_per_sec')
                opackets_per_sec = val.get('opackets_per_sec')
                link_duplex = val.get('link_duplex')
                ipackets_per_sec = val.get('ipackets_per_sec')
                driver_name = val.get('driver_name')
                opackets = val.get('opackets')
                ierrors = val.get('ierrors')
                obits_per_sec = val.get('obits_per_sec')
                rows.append(
                    [link_status, rx_nombuf, link_speed, ibytes, obytes, number, oerrors, imissed, ibits_per_sec,
                     ipackets, imissed_per_sec, opackets_per_sec, link_duplex, ipackets_per_sec, driver_name, opackets,
                     ierrors, obits_per_sec])

        elif name == 'ports_avail':
            caption = 'ports_avail'
            ports = ports_avail_get(dev.get('url'))
            columns = ['driver_name', 'duplex', 'numa', 'speed', 'status']
            for val in ports:
                driver_name = val.get('driver_name')
                duplex = val.get('duplex')
                numa = val.get('numa')
                speed = val.get('speed')
                status = val.get('status')
                rows.append([driver_name, duplex, numa, speed, status])

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
