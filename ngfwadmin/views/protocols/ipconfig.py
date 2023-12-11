
from django.shortcuts import redirect, render

from ngfwadmin.views.debug.error import exception
from ngfwadmin.views.connect.connect import get_connect
from ngfwadmin.rest.protocols.ipconfig import ipconfig_delete, ipconfig_select_all, ipconfig_insert


# Страница протокола ip
def protocol_ipconfig(request):
    try:
        # Подключение
        dev = get_connect()
        # Проверка подключения
        if 'url' not in dev:
            return redirect('connect')
        # подключение
        url = dev.get('url')
        # удалить маршрут
        port = request.GET.get("port")
        delete = request.GET.get("delete")
        if port is not None and delete is not None:
            # удалить маршрут
            ipconfig_delete(url, delete, port)
            # перейти к таблице списков
            return redirect('protocol_ipconfig')
        # Данные страницы
        ipconfig = ipconfig_select_all(url)
        context = {'dev': dev,
                   'ipconfig': ipconfig}
        # Вернуть сформированную страницу
        return render(request, 'protocols/ipconfig.html', context=context)
    except Exception as ex:
        return exception(request, ex)


def protocol_ipconfig_add(request):
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
                ip = request.POST.get('ip')
                mask = request.POST.get('mask')
                ipgw = request.POST.get('ipgw')
                port = request.POST.get('port')
                vlan = request.POST.get('vlan')
                # добавить маршрут
                ipconfig_insert(url, ip, mask, vlan, port, ipgw)
                # перейти к таблице маршрутов
                return redirect('protocol_ipconfig')
        # Вернуть сформированную страницу
        return render(request, 'protocols/ipconfig_form.html')
    except Exception as ex:
        return exception(request, ex)