import json
import requests


# Получить статус
def status_get(url, login, password):
    response = requests.get(f"{url}/router/nat/status", auth=(login, password))
    if response.status_code != 200:
        raise Exception(response.url, response.text)
    details = response.json()
    return details


# Установить статус
def status_set(url, login, password, enable):
    dic = {'nat_enable': enable}
    sjson = json.dumps(dic)
    details = json.loads(sjson)
    response = requests.put(f"{url}/router/nat/status", json=details, auth=(login, password))
    if response.status_code != 200:
        raise Exception(response.url, response.text, details)
    return response.content


# Получить порты nat
def static_port_select(url, login, password):
    response = requests.get(f"{url}/router/nat/static_port", auth=(login, password))
    if response.status_code != 200:
        raise Exception(response.url, response.text)
    details = response.json()
    return details


# Изменить порты nat
def static_port_insert(url, login, password, ip_lan, port_lan, ip_wan, port_wan, protocol):
    dic = {
        'ip_lan': str(ip_lan),
        'ip_wan': str(ip_wan),
        'port_lan': str(port_lan),
        'port_wan': str(port_wan),
        'protocol': str(protocol)}
    sjson = json.dumps(dic)
    details = json.loads(sjson)
    response = requests.post(f"{url}/router/nat/static_port", json=details, auth=(login, password))
    if response.status_code != 200:
        raise Exception(response.url, response.text, details)
    return response.content


# Удалить  порты nat
def static_port_delete(url, login, password, id):
    response = requests.delete(f"{url}/router/nat/static_port/" + str(id), auth=(login, password))
    if response.status_code != 200:
        raise Exception(response.url, response.text)
    return response.content