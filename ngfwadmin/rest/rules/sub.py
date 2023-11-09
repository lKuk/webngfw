import json
import requests


# Добавить подправило
def sub_insert(url, idrule, arid, fidorval, isinvert):
    dic = {
        'ar_id': arid,
        'is_invert': isinvert,
        'fid_or_val': fidorval}
    sjson = json.dumps(dic)
    details = json.loads(sjson)
    response = requests.post(f"{url}/rules/{idrule}/sub", json=details)
    if response.status_code != 200:
        raise Exception(response.url, response.text)
    return response.content


# Изменить подправило
def sub_update(url, idrule, idsub, arid, fidorval, isinvert):
    dic = {
        'id': idsub,
        'ar_id': arid,
        'is_invert': isinvert,
        'fid_or_val': fidorval}
    sjson = json.dumps(dic)
    details = json.loads(sjson)
    response = requests.put(f"{url}/rules/{idrule}/sub/{idsub}", json=details)
    if response.status_code != 200:
        raise Exception(response.url, response.text)
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
