import json
import requests


# Добавить список
def list_insert(url, ftype, description):
    dic = {
        'ftype': ftype,
        'description': description}
    sjson = json.dumps(dic)
    details = json.loads(sjson)
    response = requests.post(f"{url}/rules/lists", json=details)
    if response.status_code != 200:
        raise Exception(response.url, response.text)
    return response.content


# Изменить список
def list_update(url, idlist, ftype, description):
    dic = {
        'id': idlist,
        'ftype': ftype,
        'description': description}
    sjson = json.dumps(dic)
    details = json.loads(sjson)
    response = requests.put(f"{url}/rules/lists/{idlist}/description", json=details)
    if response.status_code != 200:
        raise Exception(response.url, response.text)
    return response.content


# Удалить список
def list_delete(url, idlist):
    response = requests.delete(f"{url}/rules/lists/{idlist}")
    if response.status_code != 200:
        raise Exception(response.url, response.text)
    return response.content


# Получить список по id
def list_select(url, idlist):
    response = requests.get(f"{url}/rules/lists/{idlist}/description")
    if response.status_code != 200:
        raise Exception(response.url, response.text)
    details = response.json()
    return details


# Получить все списки
def list_select_all(url):
    response = requests.get(f"{url}/rules/lists")
    if response.status_code != 200:
        raise Exception(response.url, response.text)
    details = response.json()
    return details
