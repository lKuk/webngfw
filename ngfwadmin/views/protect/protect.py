from django.http import JsonResponse
from django.shortcuts import redirect, render

from ngfwadmin.views.connect.dev import dev_get
from ngfwadmin.views.debug.error import exception
from ngfwadmin.rest.protect.protect import get_arp_protect, set_arp
from ngfwadmin.rest.protect.protect import get_icmp_protect, set_ipmp
from ngfwadmin.rest.protect.protect import get_dhcp_snooping, set_dhcp


def protect(request):
    try:
        # Подключение
        dev = dev_get(request)
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
        limits = request.GET.get('limits')
        ports = request.GET.get('ports')
        proto = request.GET.get("proto")

        if checked is not None and proto is not None and limits is None and ports is None:
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

        if limits is not None and ports is not None and proto is not None and checked is not None:
            if proto == 'arp':
                set_arp(url, limits, ports, checked)
                return
            if proto == 'icmp':
                set_ipmp(url, limits, ports, checked)
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
