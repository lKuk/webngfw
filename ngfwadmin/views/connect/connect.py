import json
import os

from django.shortcuts import redirect, render

from ngfwadmin.forms import ConnectForm
from ngfwadmin.rest.auth import auth
from ngfwadmin.rest.auth.auth import auth_authorization
from ngfwadmin.views.connect import dev
from ngfwadmin.views.debug.error import exception
from ngfwadmin.views.connect.dev import dev_set, dev_del


# Страница подключения к устройству
def connect(request):
    try:
        result = ''
        # Удалить подключение
        dev_del(request)

        # Прочитать предварительные настройки
        settings = {}
        path = 'settings.json'
        if os.path.exists(path):
            with open(path) as f:
                settings = json.load(f)

        # Заполнить форму для метода GET
        if request.method == 'GET':
            if 'ip' in settings and 'default' in settings['ip']:
                ip = settings['ip']['default']
            if 'port' in settings and 'default' in settings['port']:
                port = settings['port']['default']
            if 'login' in settings and 'default' in settings['login']:
                login = settings['login']['default']
            if 'password' in settings and 'default' in settings['password']:
                password = settings['password']['default']
            form = ConnectForm(initial={'ip': ip, 'port': port, 'login': login, 'password': password})

        # Заполнить форму для метода POST
        if request.method == 'POST':
            form = ConnectForm(request.POST)
            # Проверка заполнения
            if form.is_valid():
                # данные формы
                obj = form.cleaned_data
                # Заполнить данные
                ip = obj['ip']
                port = obj['port']
                login = obj['login']
                password = obj['password']
                # ссылка на устройство для rest
                url = dev.get_url(ip, port)
                # запрос аутентификации
                result = auth.auth_authentication(url, login, password)
                if result.lower() == 'ok':
                    # запрос прав пользователя
                    permissions = auth_authorization(url, login, password)
                    # переформатировать привилегии для комфортного использования
                    dic_permissions = {}
                    for p in permissions:
                        method = p['method'].lower().strip()
                        path = p['path'].lower().strip().strip('/').strip('\\')
                        dic_permissions[path] = method
                    # Сохранить подключение
                    dev_set(request, ip, port, login, password, dic_permissions)
                    # Подключение выполнено
                    return redirect('state')

        # Отобразить страницу подключения
        context = {'form': form,
                   'result': result,
                   'settings': settings}
        return render(request, 'connect/connect.html', context=context)

    except Exception as ex:
        return exception(request, ex)


def welcome(request):
    try:
        # Отобразить страницу приветствия
        return render(request, 'connect/welcome.html')
    except Exception as ex:
        return exception(request, ex)
