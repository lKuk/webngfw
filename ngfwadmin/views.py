from .forms import *

from ngfwadmin.rest.rules.rules import *
from ngfwadmin.rest.rules.content import *
from ngfwadmin.rest.rules.history import *
from ngfwadmin.rest.rules.sub import *
from django.shortcuts import *

# устройство
dev = {}


# Страница подключения к устройству
def connect(request):
    try:
        if request.method == 'POST':
            form = ConnectForm(request.POST)
            if form.is_valid():
                obj = form.cleaned_data
                global dev
                ip = obj['ip']
                port = obj['port']
                login = obj['login']
                password = obj['password']
                url = 'http://' + ip + ':' + port
                dev = {'ip': ip,
                       'port': port,
                       'login': login,
                       'password': password,
                       'url': url}
                return redirect('rules')
        else:
            form = ConnectForm()
        context = {'form': form }
        return render(request, 'connect.html', context=context)
    except Exception as ex:
        return exception(request, ex)


# Страница ошибки
def error(request):
    return render(request, 'error.html', context={'name': 'Error: 404 страница не найдена'})


# Страница исключений
def exception(request, ex):
    context = {'ex': ex,
               'name': 'Exception' }
    return render(request, 'error.html', context=context)


# Страница dashboard
def dashboard(request):
    if 'url' not in dev:
        return redirect('connect')
    try:
        context = {'dev': dev}
        return render(request, 'state/dashboard.html', context=context)
    except Exception as ex:
        return exception(request, ex)




# Страница правил
def rules(request):
    try:
        # проверка подключения
        if 'url' not in dev:
            return redirect('connect')

        # подключение
        url = dev['url']

        # удалить правило
        delete = request.GET.get("delete")
        if delete is not None:
            # удалить список
            rule_delete(url, delete)
            # перейти к таблице правил
            return redirect('rules')

        # получить все правила
        all = rule_select_all(url)

        # сортировка по имени
        sort_all = sorted(all, key=lambda k: k['name'])

        # развернуть все подправила
        for rule in sort_all:
            sub_warp(url, rule)

        # отобразить страницу правил
        context = {'dev': dev,
                   'rules': sort_all}
        return render(request, 'rules/rules/rules.html', context=context)

    # обработка ошибок
    except Exception as ex:
        return exception(request, ex)


# Страница добавления правила
def rules_add(request):
    try:
        # проверка подключения
        if 'url' not in dev:
            return redirect('connect')

        # подключение
        url = dev['url']

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
                return redirect('rules_edit', id)

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
        # проверка подключения
        if 'url' not in dev:
            return redirect('connect')

        # подключение
        url = dev['url']

        # удалить подправило
        delete = request.GET.get("delete")
        if delete is not None:
            # удалить список
            sub_delete(url, id, delete)
            # перейти к таблице правил
            return redirect('rules_edit', id)

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
            # получить параметры подправила
            port = request.POST.get('port')
            invert = request.POST.get('invert')
            ip = request.POST.get('ip_address')
            mac = request.POST.get('mac_address')
            service = request.POST.get('service')
            protocol = request.POST.get('protocol')
            category = request.POST.get('category')
            # обновить правило
            if 'btnUpdate' in request.POST:
                # добавить правило
                rule_update(url, id, rtype, is_enable, name, description, sub)
                # перейти к таблице правил
                return redirect('rules')
            # добавить подправило
            if 'btnAdd' in request.POST:
                # эти параметры требуют в кавычках
                ip = "\"" + str(ip).replace("\"", "") + "\""
                mac = "\"" + str(mac).replace("\"", "") + "\""
                port = "\"" + str(port).replace("\"", "") + "\""
                # Параметры атомарного правила
                atomic = request.POST.get('atomic')
                atomic = atomic.replace("\'", "\"")
                atomic = json.loads(atomic)
                ar_id = atomic['id']
                arg_type = atomic['arg_type']
                file_type = atomic['file_type']
                # Параметры списка
                list = request.POST.get('list')
                list = list.replace("\'", "\"")
                list = json.loads(list)
                fid = list['id']
                # определить значение
                fid_or_val = ''
                if arg_type == 'IP':
                    fid_or_val = ip;
                if arg_type == 'MAC':
                    fid_or_val = mac;
                if arg_type == 'PORT':
                    fid_or_val = port
                if arg_type == 'PROTNAME':
                    fid_or_val = protocol
                if arg_type == 'CATEGNAME':
                    fid_or_val = category
                if arg_type == 'SERVICENAME':
                    fid_or_val = service
                if arg_type == 'file':
                    fid_or_val = fid
                # добавить подправило
                sub_insert(url, id, ar_id, fid_or_val, invert)
                return redirect('rules_edit', id)

        # получить данные
        rule = rule_select(url, id)
        lists = list_select_all(url)
        atomic = enum_atomic_get(url)
        service = enum_services_get(url)
        protocol = enum_protocols_get(url)
        # развернуть все подправила
        sub_warp(url, rule)

        # отобразить страницу редактирования списка
        context = {'id': id,
                   'dev': dev,
                   'rule': rule,
                   'lists': lists,
                   'atomic': atomic,
                   'service': service,
                   'protocol': protocol,
                   'action': 'edit',
                   'caption': 'Редактировать правило'}
        return render(request, 'rules/rules/rules_form.html', context=context)

    # обработка ошибок
    except Exception as ex:
        return exception(request, ex)




# Страница редактора списков
def lists(request):
    if 'url' not in dev:
        return redirect('connect')
    try:

        # подключение
        url = dev['url']
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
        lists = list_select_all(url)

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
        # проверка подключения
        if 'url' not in dev:
            return redirect('connect')

        # подключение
        url = dev['url']
        login = dev['login']
        password = dev['password']

        # создать список
        if request.method == 'POST':
            # добавить список
            if 'btnInsert' in request.POST:
                # Получить параметры
                ftype = request.POST.get('ftype')
                content = request.POST.get('content')
                description = request.POST.get('description')
                # добавить список
                result = list_insert(url, login, password, ftype, description)
                # получить id
                details = json.loads(result)
                id = details['id']
                # установить список
                content_set(url, login, password, id, content)
                # перейти к таблице списков
                return redirect('lists')

        # получить доступные форматы
        format = enum_format_ftype_get(url)

        # отобразить страницу редактирования списка
        context = {'dev': dev,
                   'format': format,
                   'action': 'add',
                   'caption': 'Добавить новый список'}
        return render(request, 'rules/lists/lists_form.html', context=context)

    # обработка ошибок
    except Exception as ex:
        return exception(request, ex)


# Страница редактора списков
def lists_edit(request, id):
    try:
        # проверка подключения
        if 'url' not in dev:
            return redirect('connect')

        # подключение
        url = dev['url']
        login = dev['login']
        password = dev['password']

        # создать список
        if request.method == 'POST':
            # Получить параметры
            ftype = request.POST.get('ftype')
            content = request.POST.get('content')
            description = request.POST.get('description')
            # обновить список
            if 'btnUpdate' in request.POST:
                # обновить список
                list_update(url, login, password, id, ftype, description)
                # установить список
                content_set(url, login, password, id, content)
                # перейти к таблице списков
                return redirect('lists')

        # получить список
        list = list_select(url, id)
        # получить содержимое списка
        content = content_get(url, id)
        # получить доступные форматы
        format = enum_format_ftype_get(url)

        # отобразить страницу редактирования списка
        context = {'dev': dev,
                   'list': list,
                   'format': format,
                   'content': content,
                   'action': 'edit',
                   'caption': 'Редактировать список'}
        return render(request, 'rules/lists/lists_form.html', context=context)

    # обработка ошибок
    except Exception as ex:
        return exception(request, ex)




# Страница истории изменений правил
def history(request):
    try:
        # проверка подключения
        if 'url' not in dev:
            return redirect('connect')

        # восстановить
        date = request.GET.get("date")
        if date is not None:
            history_set(dev['url'], date)
            return redirect('rules')

        # получить таблицу истории
        result = history_get(dev['url'])

        # преобразовать в словарь
        history = []
        for i in range(len(result['date'])):
            row = {'id': i, 'date': result['date'][i]}
            history.append(row)

        # сортировка по доте
        sorted_history = sorted(history, key=lambda k: k['date'], reverse=True)

        # отобразить страницу с историей
        context = {'dev': dev,
                   'history': sorted_history}
        return render(request, 'rules/history/history.html', context=context)

    # обработка ошибок
    except Exception as ex:
        return exception(request, ex)




# Страница таблиц Debug
def table(request, name):
    try:
        # проверка подключения
        if 'url' not in dev:
            return redirect('connect')

        # параметры таблицы
        rows = []
        columns = []
        caption = ''

        # Атомарные правила
        if name == 'atomic':
            caption = 'Атомарные правила'
            atomic = enum_atomic_get(dev['url'])
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
            formats = enum_format_get(dev['url'])
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
            services = enum_services_get(dev['url'])
            columns = ['Сервисы']
            for val in services:
                rows.append([val])

        # Список протоколов
        if name == 'protocols':
            caption = 'Список протоколов'
            protocols = enum_protocols_get(dev['url'])
            columns = ['Протоколы']
            for val in protocols:
                rows.append([val])

        # отобразить страницу с таблицей
        context = {'dev': dev,
                   'name': name,
                   'rows': rows,
                   'caption': caption,
                   'columns': columns, }
        return render(request, 'table.html', context=context)

    # обработка ошибок
    except Exception as ex:
        return exception(request, ex)











# def do_subrule_insert(connect, request, id):
#     # Получить параметры
#     port = request.POST.get('port')
#     invert = request.POST.get('invert')
#     ip = request.POST.get('ip_address')
#     mac = request.POST.get('mac_address')
#     service = request.POST.get('service')
#     protocol = request.POST.get('protocol')
#     category = request.POST.get('category')
#     # эти параметры требуют в кавычках
#     ip = "\"" + str(ip).replace("\"", "") + "\""
#     mac = "\"" + str(mac).replace("\"", "") + "\""
#     port = "\"" + str(port).replace("\"", "") + "\""

#     # Параметры атомарного правила
#     atomic = request.POST.get('atomic')
#     atomic = atomic.replace("\'", "\"")
#     atomic = json.loads(atomic)
#     ar_id = atomic['id']
#     arg_type = atomic['arg_type']
#     file_type = atomic['file_type']
#     # Параметры списка
#     list = request.POST.get('list')
#     list = list.replace("\'", "\"")
#     list = json.loads(list)
#     fid = list['id']
#     # определить значение
#     fid_or_val = ''
#     if arg_type == 'IP':
#         fid_or_val = ip;
#     if arg_type == 'MAC':
#         fid_or_val = mac;
#     if arg_type == 'PORT':
#         fid_or_val = port
#     if arg_type == 'PROTNAME':
#         fid_or_val = protocol
#     if arg_type == 'CATEGNAME':
#         fid_or_val = category
#     if arg_type == 'SERVICENAME':
#         fid_or_val = service
#     if arg_type == 'file':
#         fid_or_val = fid
#
#     result = sub_insert(connect['url'], id, ar_id, fid_or_val, invert)
#     details = json.loads(result)
#     return details['id']
# #
# def do_subrule_delete(connect, request, id):
#     # Получить параметры
#     sub_id = request.POST.get('sub_id')
#     rule_id = request.POST.get('rule_id')
#     sub_delete(connect['url'], rule_id, sub_id)
#     return

