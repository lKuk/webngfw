from django.http import JsonResponse
from django.shortcuts import redirect, render

from ngfwadmin.views.debug.error import exception
from ngfwadmin.views.connect.connect import get_connect
from ngfwadmin.rest.syslog.syslog import type_set, server_set, get_syslog_server, get_syslog_types


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


        ipServer = request.GET.get("ipServer")
        portServer = request.GET.get("portServer")
        if ipServer is not None and portServer is not None:
            server_set(url, ipServer, portServer)
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
