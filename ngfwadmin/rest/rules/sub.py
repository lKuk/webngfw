import json
import requests

from ngfwadmin.rest.rules.lists import list_select
from ngfwadmin.rest.rules.enum import enum_atomic_get, enum_format_get


# Добавить подправило
def sub_insert(url, idrule, arid, fidorval, isinvert):
    dic = {
        'ar_id': arid,
        'is_invert': str(isinvert),
        'fid_or_val': str(fidorval)}
    sjson = json.dumps(dic)
    details = json.loads(sjson)
    response = requests.post(f"{url}/rules/{idrule}/sub", json=details)
    if response.status_code != 200:
        raise Exception(response.url, response.text, details)
    return response.content


# Изменить подправило
def sub_update(url, idrule, idsub, arid, fidorval, isinvert):
    dic = {
        'id': idsub,
        'ar_id': arid,
        'is_invert': str(isinvert),
        'fid_or_val': str(fidorval)}
    sjson = json.dumps(dic)
    details = json.loads(sjson)
    response = requests.put(f"{url}/rules/{idrule}/sub/{idsub}", json=details)
    if response.status_code != 200:
        raise Exception(response.url, response.text, details)
    return response.content


# Удалить подправило
def sub_delete(url, idrule, idsub):
    response = requests.delete(f"{url}/rules/{idrule}/sub/{idsub}")
    if response.status_code != 200:
        raise Exception(response.url, response.text)
    return response.content


# Получить правило по id
def sub_select(url, idrule, idsub):
    response = requests.get(f"{url}/rules/{idrule}/sub/{idsub}")
    if response.status_code != 200:
        raise Exception(response.url, response.text)
    details = response.json()
    return details


# Наполнить подправило полями
def sub_warp(url, rule):
    try:
        atomics = enum_atomic_get(url)
        formats = enum_format_get(url)
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
            s2['ar_type'] = 'NO'
            s2['ar_format'] = 'None'
            s2['ar_description'] = 'Unknown'
            if ar_id in atomics:
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
                    s2['list_id'] = idlist
                    if list is None:
                        s2['list_name'] = 'list not found, id=' + str(idlist)
                        s2['list_description'] = 'list not found, id=' + str(idlist)
                    else:
                        s2['list_name'] = list['name']
                        s2['list_description'] = list['description']
            sub2.append(s2)
        rule['sub2'] = sub2
        return
    # обработка ошибок
    except Exception as ex:
        return
