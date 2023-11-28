from .forms import *

from django.shortcuts import *
from ngfwadmin.rest.rules.sub import *
from ngfwadmin.rest.rules.rules import *
from ngfwadmin.rest.rules.content import *
from ngfwadmin.rest.rules.history import *
from ngfwadmin.rest.system.version import *

# устройство
dev = {}
# подправило
dictsub = {}

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
                url = 'http://' + ip + ':' + str(port)
                version = version_get(url)
                dev = {'ip': ip,
                       'port': port,
                       'login': login,
                       'version': version,
                       'password': password,
                       'url': url}
                return redirect('rules')
        else:
            form = ConnectForm()
        context = {'form': form}
        return render(request, 'connect.html', context=context)
    except Exception as ex:
        return exception(request, ex)


# Страница ошибки
def error(request):
    return render(request, 'error.html', context={'name': 'Error: 404 страница не найдена'})


# Страница исключений
def exception(request, ex):
    context = {'ex': ex,
               'name': 'Exception'}
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
        # проверка подключения
        if 'url' not in dev:
            return redirect('connect')

        # подключение
        url = dev['url']

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
        # проверка подключения
        if 'url' not in dev:
            return redirect('connect')

        # подключение
        url = dev['url']
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
            if 'btnListNew'in request.POST:
                rule = rule_select(url, id)
                format = enum_format_get(url)
                context = {'dev': dev,
                           'rule': rule,
                           'ftype': ftype,
                           'format': format,
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

        # развернуть все списки
        if lists is not None:
            for list in lists:
                list_warp(url, list)

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

        # получить доступные форматы
        format = enum_format_get(url)

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
        # получить доступные форматы
        format = enum_format_get(url)
        # список сервисов
        services = enum_services_get(url)
        # список протоколов
        protocols = enum_protocols_get(url)

        # отобразить страницу редактирования списка
        context = {'dev': dev,
                   'list': list,
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
            columns = ['id', 'file_type', 'description', 'rule_category', 'arg_type']
            for i in atomic:
                row = atomic[i]
                id = row['id']
                arg_type = row['arg_type']
                file_type = row['file_type']
                description = row['description']
                rule_category = row['rule_category']
                rows.append([id, file_type, description, rule_category, arg_type])

        # Формат атомарных правил
        if name == 'format':
            caption = 'Форматы атомарных правил'
            formats = enum_format_get(dev['url'])
            columns = ['id', 'name', 'print', 'description', 'param']
            for row in formats['formats']:
                id = row['id']
                name = row['name']
                print = row['print']
                param = row['param']
                description = row['description']
                rows.append([id, name, print, description, param])

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
