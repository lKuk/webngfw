import json

from django.shortcuts import redirect, render

from ngfwadmin.views.connect.dev import dev_get
from ngfwadmin.views.debug.error import exception
from ngfwadmin.rest.rules.lists import content_set, list_update, list_select, content_get
from ngfwadmin.rest.rules.lists import list_delete, list_select_all, list_warp, list_insert
from ngfwadmin.rest.rules.enum import enum_format_get, enum_protocols_get, enum_services_get, enum_mimes_get


# Страница редактора списков
def lists(request):
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
        login = dev['login']
        password = dev['password']

        # удалить список
        delete = request.GET.get("delete")
        if delete is not None:
            # удалить список
            list_delete(url, login, password, delete)
            # перейти к таблице списков
            return redirect('lists')

        # создать таблицу списков
        lists = list_select_all(url, login, password)

        # развернуть все списки
        if lists is not None:
            for list in lists:
                list_warp(url, login, password, list)

        # отобразить страницу с таблицей списков
        context = {'dev': dev,
                   'lists': lists}
        return render(request, 'rules/lists/lists.html', context=context)

    # обработка ошибок
    except Exception as ex:
        return exception(request, ex)


# Страница добавления списка
def lists_add(request):
    try:
        # Подключение
        dev = dev_get(request)

        # Проверка подключения
        if 'url' not in dev or 'login' not in dev or 'password' not in dev:
            return redirect('connect')

        # подключение
        url = dev.get('url')
        login = dev['login']
        password = dev['password']

        # создать список
        if request.method == 'POST':
            # добавить список
            if 'btnListInsert' in request.POST:
                # Получить параметры
                name = request.POST.get('name')
                mark = request.POST.get('type')
                ftype = request.POST.get('ftype')
                content = request.POST.get('content')
                description = request.POST.get('description')
                # добавить список
                result = list_insert(url, login, password, name, ftype, mark, description)
                # получить id
                details = json.loads(result)
                id = details['id']
                # установить список
                content_set(url, login, password, id, content)
                # перейти к таблице списков
                return redirect('lists')

        # получить список mime
        mimes = enum_mimes_get(url, login, password)
        # получить доступные форматы
        format = enum_format_get(url, login, password)
        # список сервисов
        services = enum_services_get(url, login, password)
        # список протоколов
        protocols = enum_protocols_get(url, login, password)

        # отобразить страницу редактирования списка
        context = {'dev': dev,
                   'mimes': mimes,
                   'format': format,
                   'services': services,
                   'protocols': protocols,
                   'action': 'add',
                   'caption': 'Добавить новый список'}
        return render(request, 'rules/lists/lists_form.html', context=context)

    # обработка ошибок
    except Exception as ex:
        return exception(request, ex)


# Страница редактора списков
def lists_edit(request, id):
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

        # создать список
        if request.method == 'POST':
            # Получить параметры
            name = request.POST.get('name')
            mark = request.POST.get('type')
            ftype = request.POST.get('ftype')
            content = request.POST.get('content')
            description = request.POST.get('description')
            # обновить список
            if 'btnListUpdate' in request.POST:
                # обновить список
                list_update(url, login, password, id, name, ftype, mark, description)
                # установить список
                content_set(url, login, password, id, content)
                # перейти к таблице списков
                return redirect('lists')

        # получить список
        list = list_select(url, id)
        # получить содержимое списка
        content = content_get(url, id)
        # получить список mime
        mimes = enum_mimes_get(url, login, password)
        # получить доступные форматы
        format = enum_format_get(url, login, password)
        # список сервисов
        services = enum_services_get(url, login, password)
        # список протоколов
        protocols = enum_protocols_get(url, login, password)

        # отобразить страницу редактирования списка
        context = {'dev': dev,
                   'list': list,
                   'mimes': mimes,
                   'format': format,
                   'content': content,
                   'services': services,
                   'protocols': protocols,
                   'action': 'edit',
                   'caption': 'Редактировать список'}
        return render(request, 'rules/lists/lists_form.html', context=context)

    # обработка ошибок
    except Exception as ex:
        return exception(request, ex)