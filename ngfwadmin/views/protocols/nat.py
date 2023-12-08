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


def protocol_nat_add(request):
    try:
        # Подключение
        dev = get_connect()
        # Проверка подключения
        if 'url' not in dev:
            return redirect('connect')
        # подключение
        url = dev.get('url')
        # создать маршрут
        if request.method == 'POST':
            # добавить маршрут
            if 'btnInsert' in request.POST:
                # Получить параметры
                ip_lan = request.POST.get('ip_lan')
                ip_wan = request.POST.get('ip_wan')
                port_lan = request.POST.get('port_lan')
                port_wan = request.POST.get('port_wan')
                protocol = request.POST.get('protocol')
                # добавить маршрут
                static_port_insert(url, ip_lan, port_lan, ip_wan, port_wan, protocol)
                # перейти к таблице маршрутов
                return redirect('protocol_route')
        # Вернуть сформированную страницу
        return render(request, 'protocols/nat_form.html')
    except Exception as ex:
        return exception(request, ex)