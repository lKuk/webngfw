from ngfwadmin.rest.sys.sys import *
from ngfwadmin.rest.ports.ports import *
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

        # подключение
        url = dev.get('url')
        uptime = uptime_get(url)
        serial = serial_get(url)
        status = status_get(url)
        version = version_get(url)
        ram = monitoring_ram_get(url)
        disk = monitoring_disk_get(url)
        lcores = monitoring_lcores_get(url)

        context = {'dev': dev,
                   'ram': ram,
                   'disk': disk,
                   'lcores': lcores,
                   'serial': serial,
                   'uptime': uptime,
                   'status': status,
                   'version': version}
        return render(request, 'sys/sys.html', context=context)
    except Exception as ex:
        return exception(request, ex)


# Страница состояния портов
def ports(request):
    try:
        # Подключение
        dev = get_connect()

        # Проверка подключения
        if 'url' not in dev:
            return redirect('connect')

        # подключение
        url = dev.get('url')
        ports = ports_get(url)
        context = {'dev': dev,
                   'ports': ports}
        return render(request, 'sys/ports.html', context=context)
    except Exception as ex:
        return exception(request, ex)
