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
