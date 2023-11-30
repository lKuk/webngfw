from ngfwadmin.views.connect.connect import dev
from django.shortcuts import redirect, render

# Страница системы
def system(request):
    if 'url' not in dev:
        return redirect('connect')
    try:
        # подключение
        url = dev['url']

        uptime = uptime_get(url)
        serial = serial_get(url)
        lcores = lcores_get(url)
        status = status_get(url)
        ports = sys_ports_get(url)
        version = version_get(url)
        settings = settings_get(url)

        context = {'dev': dev,
                   'ports': ports,
                   'serial': serial,
                   'lcores': lcores,
                   'uptime': uptime,
                   'status': status,
                   'version': version,
                   'settings': settings}
        return render(request, 'system/system.html', context=context)
    except Exception as ex:
        return exception(request, ex)

