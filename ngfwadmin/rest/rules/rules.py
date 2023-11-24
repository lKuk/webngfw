from ngfwadmin.rest.rules.enum import *
from ngfwadmin.rest.rules.lists import *


# Добавить правило
def rule_insert(url, rtype, is_enable, name, description):
    dic = {
        'name': name,
        'rtype': rtype,
        'is_enable': is_enable,
        'description': description}
    sjson = json.dumps(dic)
    details = json.loads(sjson)
    response = requests.post(f"{url}/rules", json=details)
    if response.status_code != 200:
        raise Exception(response.url, response.text, details)
    return response.content


# Изменить правило
def rule_update(url, idrule, rtype, is_enable, name, description, sub):
    dic = {
        'id': idrule,
        'name': name,
        'rtype': rtype,
        'is_enable': is_enable,
        'description': description,
        'sub': sub}
    sjson = json.dumps(dic)
    details = json.loads(sjson)
    response = requests.put(f"{url}/rules/{idrule}", json=details)
    if response.status_code != 200:
        raise Exception(response.url, response.text, details)
    return response.content


# Удалить правило
def rule_delete(url, idrule):
    response = requests.delete(f"{url}/rules/{idrule}")
    if response.status_code != 200:
        raise Exception(response.url, response.text)
    return response.content


# Получить правило по id
def rule_select(url, idrule):
    response = requests.get(f"{url}/rules/{idrule}")
    if response.status_code != 200:
        raise Exception(response.url, response.text)
    details = response.json()
    return details


# Получить список всех правил
def rule_select_all(url):
    response = requests.get(f"{url}/rules")
    if response.status_code != 200:
        raise Exception(response.url, response.text)
    details = response.json()
    return details


# Применить изменения всех правил
def rule_apply(url):
    response = requests.put(f"{url}/rules")
    if response.status_code != 200:
        raise Exception(response.url, response.text)
    return


# Получить текущее описание правил
def rule_description(url):
    response = requests.get(f"{url}/rules/description")
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
