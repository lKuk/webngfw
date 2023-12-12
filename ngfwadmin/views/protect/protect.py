from ngfwadmin.rest.state.state import *
from ngfwadmin.views.connect.connect import *
from ngfwadmin.rest.protect.protect import *

from django.http import JsonResponse
from django.shortcuts import redirect, render


def protect(request):
    try:
        # Подключение
        dev = get_connect()
        # Проверка подключения
        if 'url' not in dev:
            return redirect('connect')

        # подключение
        url = dev.get('url')

        arp = get_arp_protect(url)
        icmp = get_icmp_protect(url)
        dhcp = get_dhcp_snooping(url)

        # изменить статус
        checked = request.GET.get("status")
        proto = request.GET.get("proto")
        if checked is not None and proto is not None:
            if proto == 'arp':
                limits = arp['limits']
                ports = arp['ports']
                set_arp(url, limits, ports, checked)
                return
            if proto == 'icmp':
                limits = icmp['limits']
                ports = icmp['ports']
                set_ipmp(url, limits, ports, checked)
                return
            if proto == 'dhcp':
                set_dhcp(url, checked)
                return
            return

        limits = request.GET.get('limits')
        ports = request.GET.get('ports')
        proto = request.GET.get("proto")
        if limits is not None and ports is not None and proto is not None:
            if proto == 'arp':
                status = arp['status']
                set_arp(url, limits, ports, status)
                return
            if proto == 'icmp':
                status = icmp['status']
                set_ipmp(url, limits, ports, status)
                return
            return


        context = {'dev': dev,
                   'arp': arp,
                   'icmp': icmp,
                   'dhcp': dhcp
                   }
        # Вернуть данные
        ajax = request.GET.get("ajax")
        if ajax is not None:
            return JsonResponse(context)
        # Вернуть сформированную страницу
        return render(request, 'protect/protect.html', context=context)
    except Exception as ex:
        return exception(request, ex)
