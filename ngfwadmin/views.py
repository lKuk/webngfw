from django.http import *
from ngfwadmin.action import *
from ngfwadmin.rest.rules.rules import *
from ngfwadmin.rest.rules.content import *
from ngfwadmin.rest.rules.history import *
from django.shortcuts import render


url = 'http://192.168.1.145:18888'


# Страница ошибки
def error(request, exception):
    return render(request, 'error.html', context={'name': 'Error: 404 страница не найдена'})


# Страница dashboard
def dashboard(request):
    try:
        return render(request, 'state/dashboard.html')
    except Exception as ex:
        return do_show_error(request, ex)


# Страница правил
def rules(request):
    try:
        if request.method == 'POST':
            # создать правило
            if 'btnInsert' in request.POST:
                do_rule_insert(url, request)
            # изменить правило
            if 'btnUpdate' in request.POST:
                do_rule_update(url, request)
            # создать правило и перейти в подправила
            if 'btnInsertGo' in request.POST:
                idrule = do_rule_insert(url, request)
                return subrules(request, idrule)
            # изменить правило и перейти в подправила
            if 'btnUpdateGo' in request.POST:
                idrule = request.POST.get('id')
                do_rule_update(url, request)
                return subrules(request, idrule)
            # удалить правило
            if 'btnDelete' in request.POST:
                do_rule_delete(url, request)
        ruleall = rule_select_all(url)
        for rule in ruleall:
            do_sub_warp(url, rule)
        context = {'rules': ruleall}
        return render(request, 'rules/rules.html', context=context)
    except Exception as ex:
        return do_show_error(request, ex)


# Страница подправила
def subrules(request, id):
    try:
        rule = rule_select(url, id)
        lists = list_select_all(url)
        atomic = enum_atomic_get(url)
        service = enum_services_get(url)
        protocol = enum_protocols_get(url)
        do_sub_warp(url, rule)
        context = {'id': id,
                   'rule': rule,
                   'lists': lists,
                   'atomic': atomic,
                   'service': service,
                   'protocol': protocol}
        return render(request, 'rules/subrules.html', context=context)
    except Exception as ex:
        return do_show_error(request, ex)


# Страница редактора списков
def lists(request):
    try:
        if request.method == 'POST':
            # создать правило
            if 'btnInsert' in request.POST:
                do_list_insert(url, request)
            # изменить правило
            if 'btnUpdate' in request.POST:
                do_list_update(url, request)
            # удалить правило
            if 'btnDelete' in request.POST:
                do_list_delete(url, request)
        listall = list_select_all(url)
        dict = enum_format_get(url)
        format = []
        for f in dict['formats']:
            name = f['name']
            if name not in format:
                format.append(name)
        context = {'lists': listall,
                   'format': format}
        return render(request, 'rules/lists.html', context=context)
    except Exception as ex:
        return do_show_error(request, ex)


# Страница редактирования содержимого
def content(request, id):
    try:
        if request.method == 'POST':
            # сохранить список
            if 'btnSet' in request.POST:
                do_content_set(url, request)
        list = list_select(url, id)
        filetext = content_get(url, id)
        context = {'id': id,
                   'list': list,
                   'filetext': filetext}
        return render(request, 'rules/content.html', context=context)
    except Exception as ex:
        return do_show_error(request, ex)


# Страница истории изменений правил
def history(request):
    try:
        # создать правило
        if 'btnRecover' in request.POST:
            do_history_recover(url, request)
            return rules(request)
        result = history_get(url)
        history = []
        for i in range(len(result['date'])):
            row = { 'id': i, 'date': result['date'][i] }
            history.append(row)
        context = {'history': history }
        return render(request, 'rules/history.html', context=context)
    except Exception as ex:
        return do_show_error(request, ex)


# Страница таблиц Debug
def table(request, name):
    try:
        rows = []
        columns = []
        caption = ''

        # Атомарные правила
        if name == 'atomic':
            caption = 'Атомарные правила'
            atomic = enum_atomic_get(url)
            columns = ['ID', 'Название', 'Тип данных', 'Тип файла']
            for i in atomic:
                row = atomic[i]
                id = row['id']
                arg_type = row['arg_type']
                file_type = row['file_type']
                description = row['description']
                rows.append([id, description, arg_type, file_type])

        # Формат атомарных правил
        if name == 'format':
            caption = 'Форматы атомарных правил'
            formats = enum_format_get(url)
            columns = ['ID', 'Параметр', 'Название', 'Описание']
            for row in formats['formats']:
                id = row['id']
                name = row['name']
                param = row['param']
                description = row['description']
                rows.append([id, param, name, description])

        # Список сервисов
        if name == 'services':
            caption = 'Список сервисов'
            services = enum_services_get(url)
            columns = ['Сервисы']
            for val in services:
                rows.append([val])

        # Список протоколов
        if name == 'protocols':
            caption = 'Список протоколов'
            protocols = enum_protocols_get(url)
            columns = ['Протоколы']
            for val in protocols:
                rows.append([val])

        context = {'name': name,
                   'rows': rows,
                   'caption': caption,
                   'columns': columns, }
        return render(request, 'table.html', context=context)
    except Exception as ex:
        return do_show_error(request, ex)
