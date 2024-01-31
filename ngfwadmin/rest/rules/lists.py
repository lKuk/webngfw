import json
import requests


from ngfwadmin.rest.rules.enum import enum_format_get


# Добавить список
def list_insert(url, login, password, name, ftype, mark, description):
    dic = {
        'name': name,
        'type': mark,
        'ftype': ftype,
        'description': description}
    sjson = json.dumps(dic)
    details = json.loads(sjson)
    response = requests.post(f"{url}/rules/lists", json=details, auth=(login, password))
    if response.status_code != 200:
        raise Exception(response.url, response.text, details)
    return response.content


# Изменить список
def list_update(url, login, password, idlist, name, ftype, mark, description):
    dic = {
        'id': idlist,
        'name': name,
        'type': mark,
        'ftype': ftype,
        'description': description}
    sjson = json.dumps(dic)
    details = json.loads(sjson)
    response = requests.put(f"{url}/rules/lists/{idlist}/description", json=details, auth=(login, password))
    if response.status_code != 200:
        raise Exception(response.url, response.text, details)
    return response.content


# Удалить список
def list_delete(url, login, password, idlist):
    response = requests.delete(f"{url}/rules/lists/{idlist}", auth=(login, password))
    if response.status_code != 200:
        raise Exception(response.url, response.text)
    return response.content


# Получить список по id
def list_select(url, login, password, idlist):
    response = requests.get(f"{url}/rules/lists/{idlist}/description", auth=(login, password))
    if response.status_code != 200:
        raise Exception(response.url, response.text)
    details = response.json()
    return details


# Получить все списки
def list_select_all(url, login, password):
    response = requests.get(f"{url}/rules/lists", auth=(login, password))
    if response.status_code != 200:
        raise Exception(response.url, response.text)
    details = response.json()
    return details


# Установить содержимое списка
def content_set(url, login, password, idlist, filetext):
    filetext = filetext + '\n'
    buffer = bytes(filetext, 'utf-8')
    response = requests.put(f"{url}/rules/lists/{idlist}/content", data=buffer, auth=(login, password))
    if response.status_code != 200:
        raise Exception(response.url, response.text)
    return response.content


# Получить содержимое списка
def content_get(url, login, password, idlist):
    response = requests.get(f"{url}/rules/lists/{idlist}/content", auth=(login, password))
    if response.status_code != 200:
        return ''
    details = response.text.rstrip('\n')
    return details


# Наполнить список
def list_warp(url, login, password, list):
    try:
        formats = enum_format_get(url, login, password)
        # Заполнить параметры формата файла
        for f in formats['formats']:
            if f['name'].upper() == list['ftype'].upper():
                list['fprint'] = f['print']
                break
        return
    # обработка ошибок
    except Exception as ex:
        return

