
from django.http import JsonResponse
from django.shortcuts import redirect, render

from ngfwadmin.rest.ports.ports import ports_get, get_mgmnt_stat, get_graylog_stat
from ngfwadmin.views.connect.dev import dev_get
from ngfwadmin.views.debug.error import exception


# Страница состояния портов
def ports(request):
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

        port = ports_get(url, login, password)
        graylog = get_graylog_stat(url, login, password)
        mgmnt_stat = get_mgmnt_stat(url, login, password)

        context = {'dev': dev,
                   'ports': port,
                   'mgmnt_stat': mgmnt_stat,
                   'graylog': graylog}
        # Вернуть данные
        ajax = request.GET.get("ajax")
        if ajax is not None:
            return JsonResponse(context)
        # Вернуть сформированную страницу
        return render(request, 'ports/ports.html', context=context)
    except Exception as ex:
        return exception(request, ex)
