from django.http import HttpResponse
from django.shortcuts import render

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
def do_sub_warp(url, rule):
    atomics = enum_atomic_get(url)
    formats = enum_format_get(url)
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
                    list = list_select(url, idlist)
                    s2['list_description'] = list['description']
            sub2.append(s2)
        rule['sub2'] = sub2
    except Exception as e:
        return HttpResponse(e)
    return


def do_rule_insert(url, request):
    # Получить параметры
    name = request.POST.get('name')
    rtype = request.POST.get('rtype')
    is_enable = request.POST.get('is_enable')
    description = request.POST.get('description')
    # добавить правило
    result = rule_insert(url, rtype, is_enable, name, description)
    details = json.loads(result)
    return details['id']


def do_rule_update(url, request):
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
    rule_update(url, id, rtype, is_enable, name, description, sub)
    return


def do_rule_delete(url, request):
    # Получить id
    id = request.POST.get('id')
    # удалить правило
    rule_delete(url, id)
    return


def do_list_insert(url, request):
    # Получить параметры
    ftype = request.POST.get('rtype')
    description = request.POST.get('description')
    # добавить список
    result = list_insert(url, ftype, description)
    details = json.loads(result)
    return details['id']


def do_list_update(url, request):
    # Получить параметры
    id = request.POST.get('id')
    ftype = request.POST.get('ftype')
    description = request.POST.get('description')
    # обновить список
    list_update(url, id, ftype, description)
    return


def do_list_delete(url, request):
    # Получить id
    id = request.POST.get('id')
    # удалить список
    list_delete(url, id)
    return


def do_content_set(url, request):
    # Получить id
    id = request.POST.get('id')
    # Получить текст списка
    filetext = request.POST.get('filetext')
    # установить список
    content_set(url, id, filetext)
    return


def do_history_recover(url, request):
    # Получить id
    date = request.POST.get('date')
    # удалить правило
    history_set(url, date)
    return
