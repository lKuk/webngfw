import json
import requests


# Вход в систему
def auth_logon(url, login, password):
    response = requests.get(f"{url}/auth", auth=(login, password), verify=False)
    if response.status_code == 401:
        return response.text
    if response.status_code != 200:
        raise Exception(response.url, response.text)
    return 'ok'


# получить список пользователей
def auth_users_get(url, login, password):
    response = requests.get(f"{url}/auth/users", auth=(login, password), verify=False)
    if response.status_code != 200:
        raise Exception(response.url, response.text)
    details = response.json()
    return details


# установить пользователя
def auth_users_set(url, login, password, log, pwd):
    dic = {'log': log, 'pass': pwd}
    sjson = json.dumps(dic)
    details = json.loads(sjson)
    response = requests.put(f"{url}/auth/users/passwd", json=details, auth=(login, password), verify=False)
    if response.status_code != 200:
        raise Exception(response.url, response.text)
    return response.content


# установить пользователя
def auth_permissions_get(url, login, password):
    response = requests.get(f"{url}/auth/users/permissions", auth=(login, password), verify=False)
    if response.status_code != 200:
        raise Exception(response.url, response.text)
    details = response.json()
    return details