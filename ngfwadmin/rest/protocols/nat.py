import json
import requests


# Получить статус
def status_get(url):
    response = requests.get(f"{url}/router/nat/status")
    if response.status_code != 200:
        raise Exception(response.url, response.text)
    details = response.json()
    return details


# Установить статус
def status_set(url, enable):
    dic = {'nat_enable': enable}
    sjson = json.dumps(dic)
    details = json.loads(sjson)
    response = requests.put(f"{url}/router/nat/status", json=details)
    if response.status_code != 200:
        raise Exception(response.url, response.text, details)
    return response.content


# Получить порты nat
def static_port_select(url):
    response = requests.get(f"{url}/router/nat/static_port")
    if response.status_code != 200:
        raise Exception(response.url, response.text)
    details = response.json()
    return details


# Изменить  порты nat
def static_port_insert(url, ip_lan, port_lan, ip_wan, port_wan, protocol):
    dic = {
        'ip_lan': str(ip_lan),
        'ip_wan': str(ip_wan),
        'port_lan': str(port_lan),
        'port_wan': str(port_wan),
        'protocol': str(protocol)}
    sjson = json.dumps(dic)
    details = json.loads(sjson)
    response = requests.post(f"{url}/router/nat/static_port", json=details)
    if response.status_code != 200:
        raise Exception(response.url, response.text, details)
    return response.content


# Удалить  порты nat
def static_port_delete(url, id):
    response = requests.delete(f"{url}/router/nat/static_port" + str(id))
    if response.status_code != 200:
        raise Exception(response.url, response.text)
    return response.content