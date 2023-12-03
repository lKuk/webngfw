
from django.shortcuts import redirect, render

from ngfwadmin.rest.protocols.ip_route import *
from ngfwadmin.views.debug.error import exception
from ngfwadmin.views.connect.connect import get_connect


# Страница протокола ip
def protocol_ip_route(request):
    try:
        # Подключение
        dev = get_connect()
        # Проверка подключения
        if 'url' not in dev:
            return redirect('connect')
        # подключение
        url = dev.get('url')
        # удалить маршрут
        delete = request.GET.get("delete")
        if delete is not None:
            # удалить маршрут
            ip_router_delete(url, delete)
            # перейти к таблице списков
            return redirect('protocol_ip_route')
        # Данные страницы
        route = ip_router_select_all(url)
        context = {'dev': dev,
                   'route': route}
        # Вернуть сформированную страницу
        return render(request, 'protocols/ip/ip_route.html', context=context)
    except Exception as ex:
        return exception(request, ex)


def protocol_ip_route_add(request):
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
                port = request.POST.get('port')
                ipgw = request.POST.get('ipgw')
                vlan = request.POST.get('vlan')
                # добавить маршрут
                ip_router_insert(url, ip, port, ipgw, vlan)
                # перейти к таблице маршрутов
                return redirect('ip_router')
        # Вернуть сформированную страницу
        return render(request, 'protocols/ip/ip_route_form.html')
    except Exception as ex:
        return exception(request, ex)


# Страница протокола ip
def protocol_ip_config(request):
    try:
        # Подключение
        dev = get_connect()
        # Проверка подключения
        if 'url' not in dev:
            return redirect('connect')
        # подключение
        url = dev.get('url')
        # Данные страницы
        context = {'dev': dev}
        # Вернуть сформированную страницу
        return render(request, 'protocols/ip/ip_config.html', context=context)
    except Exception as ex:
        return exception(request, ex)


# Страница протокола arp
def protocol_arp(request):
    try:
        # Подключение
        dev = get_connect()
        # Проверка подключения
        if 'url' not in dev:
            return redirect('connect')
        # подключение
        url = dev.get('url')
        # Данные страницы
        context = {'dev': dev}
        # Вернуть сформированную страницу
        return render(request, 'protocols/arp.html', context=context)
    except Exception as ex:
        return exception(request, ex)


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
        # Данные страницы
        context = {'dev': dev}
        # Вернуть сформированную страницу
        return render(request, 'protocols/nat.html', context=context)
    except Exception as ex:
        return exception(request, ex)


# Страница протокола icmp
def protocol_icmp(request):
    try:
        # Подключение
        dev = get_connect()
        # Проверка подключения
        if 'url' not in dev:
            return redirect('connect')
        # подключение
        url = dev.get('url')
        # Данные страницы
        context = {'dev': dev}
        # Вернуть сформированную страницу
        return render(request, 'protocols/icmp.html', context=context)
    except Exception as ex:
        return exception(request, ex)


# Страница протокола dhcp
def protocol_dhcp(request):
    try:
        # Подключение
        dev = get_connect()
        # Проверка подключения
        if 'url' not in dev:
            return redirect('connect')
        # подключение
        url = dev.get('url')
        # Данные страницы
        context = {'dev': dev}
        # Вернуть сформированную страницу
        return render(request, 'protocols/dhcp.html', context=context)
    except Exception as ex:
        return exception(request, ex)