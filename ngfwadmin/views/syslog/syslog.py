from ngfwadmin.rest.state.state import *
from ngfwadmin.views.connect.connect import *
from ngfwadmin.rest.syslog.syslog import *

from django.http import JsonResponse
from django.shortcuts import redirect, render


def syslog(request):
    try:
        # Подключение
        dev = get_connect()
        # Проверка подключения
        if 'url' not in dev:
            return redirect('connect')
        # подключение
        url = dev.get('url')
        server = get_syslog_server(url)
        context = {'dev': dev,
                   'server': server,
                   }
        # Вернуть данные
        ajax = request.GET.get("ajax")
        if ajax is not None:
            return JsonResponse(context)
        # Вернуть сформированную страницу
        return render(request, 'syslog/syslog.html', context=context)
    except Exception as ex:
        return exception(request, ex)
