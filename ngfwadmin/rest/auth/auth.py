import json
import requests


# процедура проверки подлинности пользователя
def auth_authentication(url, login, password):
    response = requests.get(f"{url}/auth/authentication", auth=(login, password), verify=False)
    if response.status_code == 401:
        return response.text
    if response.status_code != 200:
        raise Exception(response.url, response.text)
    return 'ok'


# предоставление прав на выполнение определённых действий
def auth_authorization(url, login, password):
    response = requests.get(f"{url}/auth/authorization", auth=(login, password), verify=False)
    if response.status_code != 200:
        raise Exception(response.url, response.text)
    details = response.json()
    return details


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
