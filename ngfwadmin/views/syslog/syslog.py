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

        # изменить статус
        checked = request.GET.get("checked")
        typesys = request.GET.get("typesys")
        if checked is not None and typesys is not None:
            type_set(url, checked, typesys)
            return

        server = get_syslog_server(url)
        types = get_syslog_types(url)
        context = {'dev': dev,
                   'server': server,
                   'types': types
                   }
        # Вернуть данные
        ajax = request.GET.get("ajax")
        if ajax is not None:
            return JsonResponse(context)
        # Вернуть сформированную страницу
        return render(request, 'syslog/syslog.html', context=context)
    except Exception as ex:
        return exception(request, ex)
