from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect, render

from ngfwadmin.views.connect.dev import dev_get
from ngfwadmin.views.debug.error import exception
from ngfwadmin.rest.protocols.arp import arp_select, arp_clear
from ngfwadmin.rest.service.ntp import ntp_server_get, ntp_status_get


# Страница протокола arp
def ntp(request):
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

        server = ntp_server_get(url, login, password)
        status = ntp_status_get(url, login, password)

        # Данные страницы
        context = {'dev': dev,
                   'server': server,
                   'status': status,
                   }
        # Вернуть сформированную страницу
        return render(request, 'service/ntp.html', context=context)
    except Exception as ex:
        return exception(request, ex)
