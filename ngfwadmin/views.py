from .forms import *

from ngfwadmin.action import *
from ngfwadmin.rest.rules.rules import *
from ngfwadmin.rest.rules.content import *
from ngfwadmin.rest.rules.history import *
from django.shortcuts import *


# подключение к устройству
connect = {}


# Страница подключения к устройству
def device(request):
    try:
        if request.method == 'POST':
            form = DeviceForm(request.POST)
            if form.is_valid():
                obj = form.cleaned_data
                global connect
                ip = obj['ip']
                port = obj['port']
                login = obj['login']
                password = obj['password']
                url = 'http://' + ip + ':' + port
                connect = {'ip': ip,
                           'port': port,
                           'login': login,
                           'password': password,
                           'url': url}
                return redirect('rules')
        else:
            form = DeviceForm()
        context = {'form': form}
        return render(request, 'device.html', context=context)
    except Exception as ex:
        return do_show_error(request, ex)


# Страница ошибки
def error(request, exception):
    return render(request, 'error.html', context={'name': 'Error: 404 страница не найдена'})


# Страница dashboard
def dashboard(request):
    if 'url' not in connect:
        return redirect('device')
    try:
        return render(request, 'state/dashboard.html')
    except Exception as ex:
        return do_show_error(request, ex)


# Страница правил
def rules(request):
    if 'url' not in connect:
        return redirect('device')
    try:
        if request.method == 'POST':
            # создать правило
            if 'btnInsert' in request.POST:
                do_rule_insert(connect['url'], request)
            # изменить правило
            if 'btnUpdate' in request.POST:
                do_rule_update(connect['url'], request)
            # создать правило и перейти в подправила
            if 'btnInsertGo' in request.POST:
                idrule = do_rule_insert(connect['url'], request)
                return subrules(request, idrule)
            # изменить правило и перейти в подправила
            if 'btnUpdateGo' in request.POST:
                idrule = request.POST.get('id')
                do_rule_update(connect['url'], request)
                return subrules(request, idrule)
            # удалить правило
            if 'btnDelete' in request.POST:
                do_rule_delete(connect['url'], request)
        ruleall = rule_select_all(connect['url'])
        # сортировка списков
        sorted_ruleall = sorted(ruleall, key=lambda k: k['name'])
        for rule in ruleall:
            do_sub_warp(connect, rule)
        context = {'rules': sorted_ruleall}
        return render(request, 'rules/rules/rules.html', context=context)
    except Exception as ex:
        return do_show_error(request, ex)


# Страница подправила
def subrules(request, id):
    if 'url' not in connect:
        return redirect('device')
    try:
        if request.method == 'POST':
            # создать подправило
            if 'btnInsert' in request.POST:
                do_subrule_insert(connect['url'], request, id)
            # создать подправило
            if 'btnDelete' in request.POST:
                do_subrule_delete(connect['url'], request, id)
        # Получить зависимости
        rule = rule_select(connect['url'], id)
        lists = list_select_all(connect['url'])
        atomic = enum_atomic_get(connect['url'])
        service = enum_services_get(connect['url'])
        protocol = enum_protocols_get(connect['url'])
        do_sub_warp(connect, rule)
        # сортировка списков
        sorted_lists = sorted(lists, key=lambda k: k['ftype'])
        # содержимое данных
        context = {'id': id,
                   'rule': rule,
                   'atomic': atomic,
                   'service': service,
                   'protocol': protocol,
                   'lists': sorted_lists,}
        return render(request, 'rules/subrules/subrules.html', context=context)
    except Exception as ex:
        return do_show_error(request, ex)


# Страница редактора списков
def lists(request):
    if 'url' not in connect:
        return redirect('device')
    try:
        if request.method == 'POST':
            # создать правило
            if 'btnInsert' in request.POST:
                do_list_insert(connect['url'], request)
            # изменить правило
            if 'btnUpdate' in request.POST:
                do_list_update(connect['url'], request)
            # удалить правило
            if 'btnDelete' in request.POST:
                do_list_delete(connect['url'], request)
        listall = list_select_all(connect['url'])
        dict = enum_format_get(connect['url'])
        format = []
        for f in dict['formats']:
            name = f['name']
            if name not in format:
                format.append(name)
        context = {'lists': listall,
                   'format': format}
        return render(request, 'rules/lists/lists.html', context=context)
    except Exception as ex:
        return do_show_error(request, ex)


# Страница редактирования содержимого
def content(request, id):
    if 'url' not in connect:
        return redirect('device')
    try:
        if request.method == 'POST':
            # сохранить список
            if 'btnSet' in request.POST:
                do_content_set(connect, request)
                return lists(request)
        list = list_select(connect['url'], id)
        filetext = content_get(connect['url'], id)
        context = {'id': id,
                   'list': list,
                   'filetext': filetext}
        return render(request, 'rules/lists/lists_content.html', context=context)
    except Exception as ex:
        return do_show_error(request, ex)


# Страница истории изменений правил
def history(request):
    if 'url' not in connect:
        return redirect('device')
    try:
        # создать правило
        if 'btnRecover' in request.POST:
            do_history_recover(connect, request)
            return rules(request)
        result = history_get(connect['url'])
        history = []
        for i in range(len(result['date'])):
            row = { 'id': i, 'date': result['date'][i] }
            history.append(row)
        context = {'history': history }
        return render(request, 'rules/history/history.html', context=context)
    except Exception as ex:
        return do_show_error(request, ex)


# Страница таблиц Debug
def table(request, name):
    if 'url' not in connect:
        return redirect('device')
    try:
        rows = []
        columns = []
        caption = ''

        # Атомарные правила
        if name == 'atomic':
            caption = 'Атомарные правила'
            atomic = enum_atomic_get(connect['url'])
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
            formats = enum_format_get(connect['url'])
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
            services = enum_services_get(connect['url'])
            columns = ['Сервисы']
            for val in services:
                rows.append([val])

        # Список протоколов
        if name == 'protocols':
            caption = 'Список протоколов'
            protocols = enum_protocols_get(connect['url'])
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
