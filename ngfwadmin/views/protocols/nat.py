from django.shortcuts import redirect, render

from ngfwadmin.views.connect.dev import dev_get
from ngfwadmin.views.debug.error import exception
from ngfwadmin.rest.inspection.inspection import status_set
from ngfwadmin.rest.protocols.nat import static_port_delete, status_get, static_port_select, static_port_insert


# Страница протокола nat
def protocol_nat(request):
    try:
        # Подключение
        dev = dev_get(request)
        # Проверка подключения
        if 'url' not in dev or 'login' not in dev or 'password' not in dev:
            return redirect('connect')
        # подключение
        url = dev.get('url')
        login = dev.get('login')
        password = dev.get('password')

        # изменить статус
        checked = request.GET.get("checked")
        if checked is not None:
            status_set(url, checked)
            return

        # удалить nat
        delete = request.GET.get("delete")
        if delete is not None:
            # удалить маршрут
            static_port_delete(url, delete)
            # перейти к таблице списков
            return redirect('protocol_nat')

        # Получить данные
        status = status_get(url, login, password)
        static_port = static_port_select(url, login, password)

        # Данные страницы
        context = {'dev': dev,
                   'status': status,
                   'static_port': static_port}
        # Вернуть сформированную страницу
        return render(request, 'protocols/nat/nat.html', context=context)
    except Exception as ex:
        return exception(request, ex)


def protocol_nat_add(request):
    try:
        # Подключение
        dev = dev_get(request)
        # Проверка подключения
        if 'url' not in dev or 'login' not in dev or 'password' not in dev:
            return redirect('connect')
        # подключение
        url = dev.get('url')
        login = dev.get('login')
        password = dev.get('password')
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
                return redirect('protocol_nat')
        # Данные страницы
        context = {'dev': dev}
        # Вернуть сформированную страницу
        return render(request, 'protocols/nat/nat_form.html', context=context)
    except Exception as ex:
        return exception(request, ex)