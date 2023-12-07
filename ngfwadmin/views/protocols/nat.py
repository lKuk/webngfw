from django.shortcuts import redirect, render
from ngfwadmin.views.debug.error import exception

from ngfwadmin.rest.protocols.nat import *
from ngfwadmin.views.connect.connect import *

# Страница протокола nat
def protocol_nat(request):
    try:
        # Подключение
        dev = get_connect()
        # Проверка подключения
        if 'url' not in dev:
            return redirect('connect')
        # подключение
        url = dev.get('url')

        # изменить статус
        checked = request.GET.get("checked")
        if checked is not None:
            status_set(url, checked)
            return

        status = status_get(url)
        static_port = static_port_select(url)

        # Данные страницы
        context = {'dev': dev,
                   'status': status,
                   'static_port': static_port}
        # Вернуть сформированную страницу
        return render(request, 'protocols/nat.html', context=context)
    except Exception as ex:
        return exception(request, ex)
