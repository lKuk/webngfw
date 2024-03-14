from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect, render

from ngfwadmin.views.connect.dev import dev_get
from ngfwadmin.views.debug.error import exception
from ngfwadmin.rest.service.ldap import colector_get, users_get, collector_put, user_insert, user_delete


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

        # удалить пользователя
        delete = request.GET.get("delete")
        if delete is not None:
            user_delete(url, login, password, delete)
            # перейти к таблице правил
            return redirect('ldap')
        # ldap
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


# Страница добавления пользователя
def user_add(request):
    try:
        # Подключение
        dev = dev_get(request)

        # проверка подключения
        if 'url' not in dev or 'login' not in dev or 'password' not in dev:
            return redirect('connect')

        # подключение
        url = dev.get('url')
        login = dev.get('login')
        password = dev.get('password')

        if request.method == 'POST':
            ip = request.POST.get('ip')
            loginLDAP = request.POST.get('login')
            group = request.POST.get('group')
            user_insert(url, login, password, ip, loginLDAP, group)
            return redirect('ldap')
        # отобразить страницу редактирования списка
        context = {'dev': dev,
                   'action': 'add',
                   'caption': 'Добавить пользователя'}
        return render(request, 'service/ldap_form.html', context=context)

    # обработка ошибок
    except Exception as ex:
        return exception(request, ex)
