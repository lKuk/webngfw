from django.http import HttpResponse
from django.shortcuts import render

from ngfwadmin.rest.rules.sub import *
from ngfwadmin.rest.rules.enum import *
from ngfwadmin.rest.rules.lists import *
from ngfwadmin.rest.rules.rules import *
from ngfwadmin.rest.rules.content import *
from ngfwadmin.rest.rules.history import *


def do_show_error(request, ex):
    context = {'ex': ex,
               'name': 'Exception' }
    return render(request, 'error.html', context=context)


# Наполнить подправило полями
def do_sub_warp(connect, rule):
    atomics = enum_atomic_get(connect['url'])
    formats = enum_format_get(connect['url'])
    try:
        sub2 = []
        sub = rule['sub']
        for s in sub:
            # Атомарное
            id = s['id']
            ar_id = s['ar_id']
            is_invert = s['is_invert']
            fid_or_val = s['fid_or_val']
            # Расширение
            s2 = {}
            # Заполнить расширение
            s2['id'] = id
            s2['ar_id'] = ar_id
            s2['is_invert'] = is_invert
            s2['fid_or_val'] = fid_or_val
            s2['ar_type'] = atomics[ar_id]['file_type']
            s2['ar_format'] = atomics[ar_id]['arg_type']
            s2['ar_description'] = atomics[ar_id]['description']
            # Заполнить параметры формата атомарного правила
            s2['ar_format_description'] = ""
            for f in formats['formats']:
                name = f['name']
                param = f['param']
                if s2['ar_type'] == name:
                    if s2['ar_format'] == param:
                        s2['ar_format_description'] = f['description']
                        break
            # Заполнить параметры списка
            s2['list_description'] = ''
            if fid_or_val.isdigit():
                if s2['ar_format'] == 'file':
                    idlist = int(fid_or_val)
                    list = list_select(connect['url'], idlist)
                    s2['list_id'] = list['id']
                    s2['list_description'] = list['description']
            sub2.append(s2)
        rule['sub2'] = sub2
    except Exception as e:
        return HttpResponse(e)
    return


def do_rule_insert(connect, request):
    # Получить параметры
    name = request.POST.get('name')
    rtype = request.POST.get('rtype')
    is_enable = request.POST.get('is_enable')
    description = request.POST.get('description')
    # добавить правило
    result = rule_insert(connect['url'], rtype, is_enable, name, description)
    details = json.loads(result)
    return details['id']


def do_rule_update(connect, request):
    # Получить параметры
    id = request.POST.get('id')
    sub = request.POST.get('sub')
    name = request.POST.get('name')
    rtype = request.POST.get('rtype')
    is_enable = request.POST.get('is_enable')
    description = request.POST.get('description')
    sub = sub.replace("\'", "\"")
    sub = json.loads(sub)
    # обновить правило
    rule_update(connect['url'], id, rtype, is_enable, name, description, sub)
    return


def do_rule_delete(connect, request):
    # Получить id
    id = request.POST.get('id')
    # удалить правило
    rule_delete(connect['url'], id)
    return


def do_subrule_insert(connect, request, id):
    # Получить параметры
    port = request.POST.get('port')
    invert = request.POST.get('invert')
    ip = request.POST.get('ip_address')
    mac = request.POST.get('mac_address')
    service = request.POST.get('service')
    protocol = request.POST.get('protocol')
    category = request.POST.get('category')
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

    result = sub_insert(connect['url'], id, ar_id, fid_or_val, invert)
    details = json.loads(result)
    return details['id']


def do_subrule_delete(connect, request, id):
    # Получить параметры
    sub_id = request.POST.get('sub_id')
    rule_id = request.POST.get('rule_id')
    sub_delete(connect['url'], rule_id, sub_id)
    return


def do_list_insert(connect, request):
    # Получить параметры
    ftype = request.POST.get('ftype')
    description = request.POST.get('description')
    # добавить список
    result = list_insert(connect['url'], connect['login'], connect['passw0rd'], ftype, description)
    details = json.loads(result)
    return details['id']


def do_list_update(connect, request):
    # Получить параметры
    id = request.POST.get('id')
    ftype = request.POST.get('ftype')
    description = request.POST.get('description')
    # обновить список
    list_update(connect['url'], connect['login'], connect['passw0rd'], id, ftype, description)
    return


def do_list_delete(connect, request):
    # Получить id
    id = request.POST.get('id')
    # удалить список
    list_delete(connect['url'], connect['login'], connect['passw0rd'], id)
    return


def do_content_set(connect, request):
    # Получить id
    id = request.POST.get('id')
    # Получить текст списка
    filetext = request.POST.get('filetext')
    # установить список
    content_set(connect['url'], connect['login'], connect['passw0rd'], id, filetext)
    return


def do_history_recover(connect, request):
    # Получить id
    date = request.POST.get('date')
    # удалить правило
    history_set(connect['url'], date)
    return
