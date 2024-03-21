from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect, render

from ngfwadmin.views.connect.dev import dev_get
from ngfwadmin.views.debug.error import exception
from ngfwadmin.rest.service.ntp import ntp_server_get, ntp_status_get, ntp_server_add, ntp_server_delete


# Страница конфигурации ntp
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

        # удалить пользователя
        delete = request.GET.get("delete")
        if delete is not None:
            ntp_server_delete(url, login, password, delete)
            # перейти к таблице правил
            return redirect('ntp')

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


# Страница серверов ntp
def ntp_servers(request):
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

        # удалить пользователя
        delete = request.GET.get("delete")
        if delete is not None:
            ntp_server_delete(url, login, password, delete)
            # перейти к таблице правил
            return redirect('ntp_servers')

        server = ntp_server_get(url, login, password)
        status = ntp_status_get(url, login, password)

        # Данные страницы
        context = {'dev': dev,
                   'server': server,
                   'status': status,
                   }
        # Вернуть сформированную страницу
        return render(request, 'service/ntp_servers.html', context=context)
    except Exception as ex:
        return exception(request, ex)


# Страница добавления пользователя
def client_add(request):
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
            prefer = request.POST.get('prefer')
            ntp_server_add(url, login, password, ip, prefer)
            return redirect('ntp_servers')
        # отобразить страницу редактирования списка
        context = {'dev': dev,
                   'action': 'add',
                   'caption': 'Добавить сервер NTP'}
        return render(request, 'service/ntp_form.html', context=context)

    # обработка ошибок
    except Exception as ex:
        return exception(request, ex)