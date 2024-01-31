
from django.shortcuts import redirect, render

from ngfwadmin.views.connect.dev import dev_get
from ngfwadmin.views.debug.error import exception
from ngfwadmin.rest.protocols.dhcp import dhcp_table_select, get_table_status, set_table_status
from ngfwadmin.rest.protocols.dhcp import dhcp_subnet_select, dhcp_subnet_insert, dhcp_subnet_delete, dhcp_subnet_status
from ngfwadmin.rest.protocols.dhcp import dhcp_static_select, dhcp_static_insert, dhcp_static_delete


# Страница dhcp - выданные адреса
def protocol_dhcp_table(request):
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
        table = dhcp_table_select(url, login, password)
        status_table = get_table_status(url, login, password)

        status_dhcp_table = request.GET.get("status_dhcp_table")
        if status_dhcp_table is not None:
            set_table_status(url, status_dhcp_table)
            return

        # Данные страницы
        context = {'dev': dev,
                   'table': table,
                   'status_table': status_table }
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
        if 'url' not in dev or 'login' not in dev or 'password' not in dev:
            return redirect('connect')
        # подключение
        url = dev.get('url')
        login = dev.get('login')
        password = dev.get('password')

        # изменить состояние подсети
        port = request.GET.get("port")
        vlan = request.GET.get("vlan")
        status = request.GET.get("status")
        if port is not None and vlan is not None and status is not None:
            dhcp_subnet_status(url, port, vlan, status)
            return

        # удалить подсеть
        delete = request.GET.get("delete")
        if delete is not None:
            port = request.GET.get("port")
            vlan = request.GET.get("vlan")
            ip_end = request.GET.get("ip_end")
            ip_start = request.GET.get("ip_start")
            # удалить подсеть
            dhcp_subnet_delete(url, port, vlan, ip_start, ip_end)
            # перейти к таблице списков
            return redirect('protocol_dhcp_subnet')

        table = dhcp_subnet_select(url, login, password)
        # Данные страницы
        context = {'dev': dev,
                   'table': table }
        # Вернуть сформированную страницу
        return render(request, 'protocols/dhcp/dhcp_subnet.html', context=context)
    except Exception as ex:
        return exception(request, ex)


# Страница dhcp - Добавить подсеть
def protocol_dhcp_subnet_edit(request, port, vlan):
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
        # создать подсеть
        if request.method == 'POST':
            # добавить маршрут
            if 'btnInsert' in request.POST:
                # Получить параметры
                ip_end = request.POST.get('ip_end')
                ip_start = request.POST.get('ip_start')
                status = request.POST.get('status')
                # добавить маршрут
                dhcp_subnet_insert(url, port, vlan, ip_start, ip_end, status)
                # перейти к таблице маршрутов
                return redirect('protocol_dhcp_subnet')
        # диапазон ip адресов
        ip_end = ''
        if 'ip_end' in request.GET:
            ip_end = request.GET.get('ip_end')
        ip_start = ''
        if 'ip_start' in request.GET:
            ip_start = request.GET.get('ip_start')
        # Данные страницы
        context = {'dev': dev,
                   'port': port,
                   'vlan': vlan,
                   'ip_end': ip_end,
                   'ip_start': ip_start}
        # Вернуть сформированную страницу
        return render(request, 'protocols/dhcp/dhcp_subnet_form.html', context=context)
    except Exception as ex:
        return exception(request, ex)


# Страница dhcp - Статические адреса
def protocol_dhcp_static(request):
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

        # удалить подсеть
        delete = request.GET.get("delete")
        if delete is not None:
            ip = request.GET.get("ip")
            mac = request.GET.get("mac")
            port = request.GET.get("port")
            vlan = request.GET.get("vlan")
            # удалить подсеть
            dhcp_static_delete(url, port, vlan, ip, mac)
            # перейти к таблице списков
            return redirect('protocol_dhcp_static')

        table = dhcp_static_select(url, login, password)
        # Данные страницы
        context = {'dev': dev,
                   'table': table}
        # Вернуть сформированную страницу
        return render(request, 'protocols/dhcp/dhcp_static.html', context=context)
    except Exception as ex:
        return exception(request, ex)


# Страница dhcp - Добавить статический
def protocol_dhcp_static_add(request):
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
        # создать статический
        if request.method == 'POST':
            if 'btnInsert' in request.POST:
                # Получить параметры
                ip = request.POST.get('ip')
                mac = request.POST.get('mac')
                port = request.POST.get('port')
                vlan = request.POST.get('vlan')
                # добавить маршрут
                dhcp_static_insert(url, port, vlan, ip, mac)
                # перейти к таблице маршрутов
                return redirect('protocol_dhcp_static')
        # Данные страницы
        context = {'dev': dev}
        # Вернуть сформированную страницу
        return render(request, 'protocols/dhcp/dhcp_static_form.html', context=context)
    except Exception as ex:
        return exception(request, ex)