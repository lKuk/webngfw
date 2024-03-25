from django.http import JsonResponse
from django.shortcuts import redirect, render

from ngfwadmin.views.connect.dev import dev_get
from ngfwadmin.views.debug.error import exception
from ngfwadmin.rest.bridge.bridge import get_bridge, set_bridge


def bridge(request):
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

        # изменить статус
        checked = request.GET.get("status")
        bridge = get_bridge(url, login, password)

        if checked is not None:
            set_bridge(url, login, password, checked)

        context = {'dev': dev,
                   'bridge': bridge
                   }
        # Вернуть данные
        ajax = request.GET.get("ajax")
        if ajax is not None:
            return JsonResponse(context)
        # Вернуть сформированную страницу
        return render(request, 'bridge/bridge.html', context=context)
    except Exception as ex:
        return exception(request, ex)
