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
