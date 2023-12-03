from ngfwadmin.rest.ports.ports import *
from ngfwadmin.views.connect.connect import *

from django.shortcuts import redirect, render

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
