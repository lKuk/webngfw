import json
import requests


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
