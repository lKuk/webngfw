import requests
import json


# Получить collector(порт)
def colector_get(url, login, password):
    response = requests.get(f"{url}/ldap/collector", auth=(login, password), verify=False)
    if response.status_code != 200:
        raise Exception(response.url, response.text)
    details = response.json()
    return details


# Изменить collector(порт)
def collector_put(url, login, password, port):
    dic = {
        'port': port}
    sjson = json.dumps(dic)
    details = json.loads(sjson)
    response = requests.put(f"{url}/ldap/collector", json=details, auth=(login, password), verify=False)
    if response.status_code != 200:
        raise Exception(response.url, response.text, details)
    return response.content


# Получить пользователей
def users_get(url, login, password):
    response = requests.get(f"{url}/ldap/user", auth=(login, password), verify=False)
    if response.status_code != 200:
        raise Exception(response.url, response.text)
    details = response.json()
    return details


# Добавить пользователя
def user_insert(url, login, password, ip, loginLDAP, groups):
    dic = {
        'ip': ip,
        'login': loginLDAP,
        'groups': groups,
    }
    sjson = json.dumps(dic)
    details = json.loads(sjson)
    response = requests.post(f"{url}/ldap/user", json=details, auth=(login, password), verify=False)
    if response.status_code != 200:
        raise Exception(response.url, response.text, details)
    return response.content

# Удалить пользователя
def user_delete(url, login, password, ip):
    dic = {
        'ip': ip,
    }
    sjson = json.dumps(dic)
    details = json.loads(sjson)
    response = requests.delete(f"{url}/ldap/user", json=details, auth=(login, password), verify=False)
    if response.status_code != 200:
        raise Exception(response.url, response.text)
    return response.content


# # Отправить пинг
# def ping_post(url, login, password,ipServer ,portServer, req_amount,delay):
#     dic = {"ip_or_host": ipServer, "port": int(portServer), "req_amount": int(req_amount), "delay" : int(delay)}
#     sjson = json.dumps(dic)
#     details = json.loads(sjson)
#     response = requests.post(f"{url}/service/ping", json=details, auth=(login, password), verify=False)
#     # if response.status_code != 200:
#     #     raise Exception(response.url, response.text, details)
#     return response.content
