
from django.shortcuts import redirect, render

from ngfwadmin.views.connect.dev import dev_get
from ngfwadmin.views.debug.error import exception


# Страница dhcp - выданные адреса
def protocol_dhcp_table(request):
    try:
        # Подключение
        dev = dev_get(request)
        # Проверка подключения
        if 'url' not in dev:
            return redirect('connect')
        # подключение
        url = dev.get('url')
        # Данные страницы
        context = {'dev': dev}
        # Вернуть сформированную страницу
        return render(request, 'protocols/dhcp/dhcp_table.html', context=context)
    except Exception as ex:
        return exception(request, ex)


# Страница dhcp - Настройка подсетей
def protocol_dhcp_subnet(request):
    try:
        # Подключение
        dev = dev_get(request)
        # Проверка подключения
        if 'url' not in dev:
            return redirect('connect')
        # подключение
        url = dev.get('url')
        # Данные страницы
        context = {'dev': dev}
        # Вернуть сформированную страницу
        return render(request, 'protocols/dhcp/dhcp_subnet.html', context=context)
    except Exception as ex:
        return exception(request, ex)


# Страница dhcp - Статические адреса
def protocol_dhcp_static(request):
    try:
        # Подключение
        dev = dev_get(request)
        # Проверка подключения
        if 'url' not in dev:
            return redirect('connect')
        # подключение
        url = dev.get('url')
        # Данные страницы
        context = {'dev': dev}
        # Вернуть сформированную страницу
        return render(request, 'protocols/dhcp/dhcp_static.html', context=context)
    except Exception as ex:
        return exception(request, ex)