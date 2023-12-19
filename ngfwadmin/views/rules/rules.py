import json

from django.shortcuts import redirect, render

from ngfwadmin.views.connect.dev import dev_get
from ngfwadmin.views.debug.error import exception
from ngfwadmin.rest.rules.sub import sub_warp, sub_delete, sub_insert
from ngfwadmin.rest.rules.enum import enum_format_get, enum_atomic_get, enum_services_get, enum_protocols_get, \
    enum_mimes_get
from ngfwadmin.rest.rules.lists import list_insert, content_set, list_select_all
from ngfwadmin.rest.rules.rules import rule_apply, rule_select_all, rule_delete
from ngfwadmin.rest.rules.rules import rule_description, rule_insert, rule_update, rule_select


# подправило
dictsub = {}


# Страница правил
def rules(request):
    try:
        # Подключение
        dev = dev_get(request)

        # проверка подключения
        if 'url' not in dev:
            return redirect('connect')

        # подключение
        url = dev.get('url')

        # применить настройки правил
        if request.method == 'POST':
            if 'btnApply' in request.POST:
                rule_apply(url)
                return redirect('rules')

        # удалить правило
        delete = request.GET.get("delete")
        if delete is not None:
            # удалить список
            rule_delete(url, delete)
            # перейти к таблице правил
            return redirect('rules')

        # получить все правила
        rules = rule_select_all(url)

        # Получить описание состояния
        description = rule_description(url)

        # развернуть все подправила
        if rules is not None:
            for rule in rules:
                sub_warp(url, rule)

        # отобразить страницу правил
        context = {'dev': dev,
                   'rules': rules,
                   'description': description}
        return render(request, 'rules/rules/rules.html', context=context)

    # обработка ошибок
    except Exception as ex:
        return exception(request, ex)


# Страница добавления правила
def rules_add(request):
    try:
        # Подключение
        dev = dev_get(request)

        # проверка подключения
        if 'url' not in dev:
            return redirect('connect')

        # подключение
        url = dev.get('url')

        # создать список
        if request.method == 'POST':
            # Получить параметры
            name = request.POST.get('name')
            rtype = request.POST.get('rtype')
            is_enable = request.POST.get('is_enable')
            description = request.POST.get('description')
            # добавить список
            if 'btnInsert' in request.POST:
                # добавить правило
                result = rule_insert(url, rtype, is_enable, name, description)
                # получить id
                details = json.loads(result)
                id = details['id']
                return redirect('rules_sub_edit', id)

        # отобразить страницу редактирования списка
        context = {'dev': dev,
                   'action': 'add',
                   'caption': 'Добавить новое правило'}
        return render(request, 'rules/rules/rules_form.html', context=context)

    # обработка ошибок
    except Exception as ex:
        return exception(request, ex)


# Страница редактирования правила
def rules_edit(request, id):
    try:
        # Подключение
        dev = dev_get(request)

        # проверка подключения
        if 'url' not in dev:
            return redirect('connect')

        # подключение
        url = dev.get('url')

        # создать список
        if request.method == 'POST':
            # получить параметры правила
            sub = request.POST.get('sub')
            name = request.POST.get('name')
            rtype = request.POST.get('rtype')
            is_enable = request.POST.get('is_enable')
            description = request.POST.get('description')
            if sub is not None:
                sub = sub.replace("\'", "\"")
                sub = json.loads(sub)
            # обновить правило
            if 'btnUpdate' in request.POST:
                # добавить правило
                rule_update(url, id, rtype, is_enable, name, description, sub)
                # перейти к таблице правил
                return redirect('rules')
            # обновить правило и перейти в подправила
            if 'btnUpdateGoSub' in request.POST:
                # добавить правило
                rule_update(url, id, rtype, is_enable, name, description, sub)
                # перейти к таблице правил
                return redirect('rules_sub_edit', id)

        # получить данные
        rule = rule_select(url, id)

        # отобразить страницу редактирования списка
        context = {'id': id,
                   'dev': dev,
                   'rule': rule,
                   'action': 'edit',
                   'caption': 'Редактировать правило'}
        return render(request, 'rules/rules/rules_form.html', context=context)

    # обработка ошибок
    except Exception as ex:
        return exception(request, ex)


# Страница редактирования подправил
def rules_sub_edit(request, id):
    try:
        # Подключение
        dev = dev_get(request)

        # проверка подключения
        if 'url' not in dev:
            return redirect('connect')

        # подключение
        url = dev.get('url')
        login = dev['login']
        password = dev['password']

        # удалить подправило
        delete = request.GET.get("delete")
        if delete is not None:
            # удалить список
            sub_delete(url, id, delete)
            # перейти к таблице правил
            return redirect('rules_sub_edit', id)

        # Запомнить значения
        listId = None
        global dictsub
        if request.method == 'POST':
            # Определить значения
            ftype = 'LIT'
            ar_id = request.POST.get('ar_id')
            list_id = request.POST.get('list_id')
            is_invert = request.POST.get('is_invert')
            # Параметры атомарного правила
            if ar_id is not None and ar_id != '':
                ar_id = ar_id.replace("\'", "\"")
                ar_id = json.loads(ar_id)
                ftype = ar_id['file_type']
                ar_id = ar_id['id']
            # Параметры списка
            if list_id is not None and list_id != '':
                list_id = list_id.replace("\'", "\"")
                list_id = json.loads(list_id)
                list_id = list_id['id']
            # Сохранить значения
            if ar_id is not None:
                dictsub['ar_id'] = ar_id
                dictsub['ftype'] = ftype
            if list_id is not None:
                dictsub['list_id'] = list_id
            if is_invert is not None:
                dictsub['is_invert'] = is_invert
            # добавить подправило
            if 'btnSubAdd' in request.POST:
                # добавить подправило
                sub_insert(url, id, ar_id, list_id, is_invert)
                return redirect('rules_sub_edit', id)
            # Страница нового списка
            if 'btnListNew' in request.POST:
                rule = rule_select(url, id)
                mimes = enum_mimes_get(url)
                format = enum_format_get(url)
                services = enum_services_get(url)
                protocols = enum_protocols_get(url)
                context = {'dev': dev,
                           'rule': rule,
                           'mimes': mimes,
                           'ftype': ftype,
                           'format': format,
                           'services': services,
                           'protocols': protocols,
                           'action': 'add',
                           'caption': 'Добавить новый список'}
                return render(request, 'rules/lists/lists_form.html', context=context)
            # Добавление нового списка
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
                listId = details['id']
                # установить список
                content_set(url, login, password, listId, content)

        # получить данные
        rule = rule_select(url, id)
        lists = list_select_all(url)
        atomic = enum_atomic_get(url)
        # развернуть подправило
        sub_warp(url, rule)

        # отобразить страницу редактирования списка
        context = {'id': id,
                   'dev': dev,
                   'rule': rule,
                   'lists': lists,
                   'atomic': atomic,
                   'listId': listId,
                   'dictsub': dictsub}
        return render(request, 'rules/rules/rules_sub_form.html', context=context)

    # обработка ошибок
    except Exception as ex:
        return exception(request, ex)
