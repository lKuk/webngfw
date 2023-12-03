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
        # обновляемое содержимое
        context = ports_ajax()
        # Наполнить содержимое
        context['dev'] = dev
        return render(request, 'sys/ports.html', context=context)
    except Exception as ex:
        return exception(request, ex)


# Данные для обновления портов
def ports_ajax():
    context = {}
    # Подключение
    dev = get_connect()
    if 'url' not in dev:
        return context
    try:
        # Получить данные
        url = dev.get('url')
        ports = ports_get(url)
        # Наполнить содержимое
        context['ports'] = ports
    except:
        return context
    return context