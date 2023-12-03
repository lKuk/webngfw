from ngfwadmin.rest.sys.sys import *
from ngfwadmin.views.connect.connect import *
from ngfwadmin.rest.monitoring.monitoring import *

from django.shortcuts import redirect, render


# Страница системы
def sys(request):
    try:
        # Подключение
        dev = get_connect()
        # Проверка подключения
        if 'url' not in dev:
            return redirect('connect')
        # обновляемое содержимое
        context = sys_ajax()
        # подключение
        url = dev.get('url')
        serial = serial_get(url)
        version = version_get(url)
        # Наполнить содержимое
        context['dev'] = dev
        context['serial'] = serial
        context['version'] = version
        return render(request, 'sys/sys.html', context=context)
    except Exception as ex:
        return exception(request, ex)


# Данные для обновления системы
def sys_ajax():
    context = {}
    # Подключение
    dev = get_connect()
    if 'url' not in dev:
        return context
    try:
        # Получить данные
        url = dev.get('url')
        uptime = uptime_get(url)
        status = status_get(url)
        ram = monitoring_ram_get(url)
        disk = monitoring_disk_get(url)
        lcores = monitoring_lcores_get(url)
        # Наполнить содержимое
        context['ram'] = ram
        context['disk'] = disk
        context['lcores'] = lcores
        context['uptime'] = uptime
        context['status'] = status
    except:
        return context
    return context
