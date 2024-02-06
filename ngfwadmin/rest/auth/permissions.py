import json
import requests


# kполучить таблицу всех прав всех пользователей
def permissions_get(url, login, password):
    response = requests.get(f"{url}/auth/permissions", auth=(login, password), verify=False)
    if response.status_code != 200:
        raise Exception(response.url, response.text)
    details = response.json()
    return details


def permissions_set(url, login, password, path, user, permission):
    dic = {"path": path, "permission": {user: permission}}
    sjson = json.dumps(dic)
    details = json.loads(sjson)
    response = requests.put(f"{url}/auth/permissions", json=details, auth=(login, password), verify=False)
    if response.status_code != 200:
        raise Exception(response.url, response.text, details)
    return response.content
