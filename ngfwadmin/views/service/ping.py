from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect, render

from ngfwadmin.views.connect.dev import dev_get
from ngfwadmin.views.debug.error import exception
from ngfwadmin.rest.protocols.arp import arp_select, arp_clear
from ngfwadmin.rest.service.ping import ping_post


# Страница протокола arp
def ping(request):
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
        ipServer = request.GET.get("ipServer")
        portServer = request.GET.get("portServer")
        req_amount = request.GET.get("req_amount")
        delay = request.GET.get("delay")

        if ipServer is not None and portServer is not None and req_amount is not None and delay is not None:
            response = ping_post(url, login, password, ipServer, portServer, req_amount, delay)
            response = response.decode()
            data = {'text': str(response)}
            return JsonResponse(data)

        # Данные страницы
        context = {'dev': dev,
                   }
        # Вернуть сформированную страницу
        return render(request, 'service/ping.html', context=context)
    except Exception as ex:
        return exception(request, ex)
