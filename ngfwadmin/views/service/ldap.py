from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect, render

from ngfwadmin.views.connect.dev import dev_get
from ngfwadmin.views.debug.error import exception
from ngfwadmin.rest.service.ldap import colector_get, users_get, collector_put


# Страница протокола arp
def ldap(request):
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

        collectorPut = request.GET.get("port")
        if collectorPut is not None:
            collector_put(url, login, password, collectorPut)

        #ldap
        collector = colector_get(url, login, password)
        users = users_get(url, login, password)

        # Данные страницы
        context = {'dev': dev,
                   'collector': collector,
                   'users': users
                   }
        # Вернуть сформированную страницу
        return render(request, 'service/ldap.html', context=context)
    except Exception as ex:
        return exception(request, ex)
