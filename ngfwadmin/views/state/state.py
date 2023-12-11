from django.http import JsonResponse
from django.shortcuts import redirect, render

from ngfwadmin.views.debug.error import exception
from ngfwadmin.views.connect.connect import get_connect
from ngfwadmin.rest.state.state import uptime_get, serial_get, status_get, version_get
from ngfwadmin.rest.state.monitoring import monitoring_ram_get, monitoring_disk_get, monitoring_lcores_get


# Страница системы
def state(request):
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
        # Вернуть данные
        ajax = request.GET.get("ajax")
        if ajax is not None:
            return JsonResponse(context)
        # Вернуть сформированную страницу
        return render(request, 'state/state.html', context=context)
    except Exception as ex:
        return exception(request, ex)
