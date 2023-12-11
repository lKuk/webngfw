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
        ipmp = get_icmp_protect(url)
        dhcp = get_dhcp_snooping(url)

        context = {'dev': dev,
                   'arp': arp,
                   'ipmp': ipmp,
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
