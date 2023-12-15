
from django.shortcuts import redirect, render

from ngfwadmin.views.connect.dev import dev_get
from ngfwadmin.views.debug.error import exception
from ngfwadmin.rest.protocols.dhcp import dhcp_table_select, get_table_status, set_table_status


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
        table = dhcp_table_select(url)
        status_table = get_table_status(url)

        status_dhcp_table = request.GET.get("status_dhcp_table")
        if status_dhcp_table is not None:
            set_table_status(url, status_dhcp_table)
            return

        # Данные страницы
        context = {'dev': dev,
                   'table': table,
                   'status_table': status_table}
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