import json
import requests


# Получить статус
def status_get(url):
    response = requests.get(f"{url}/ipsids/status")
    if response.status_code != 200:
        raise Exception(response.url, response.text)
    details = response.json()
    return details


# Получить правила
def rules_get(url):
    response = requests.get(f"{url}/ipsids/rules")
    if response.status_code != 200:
        raise Exception(response.url, response.text)
    details = response.text
    return details


# Получить конфигурацию
def configuration_get(url):
    response = requests.get(f"{url}/ipsids/configuration")
    if response.status_code != 200:
        raise Exception(response.url, response.text)
    details = response.text
    return details


# Изменить список
def status_set(url, status):
    dic = {'ipsids_enable': status}
    sjson = json.dumps(dic)
    details = json.loads(sjson)
    response = requests.put(f"{url}/ipsids/status", json=details)
    if response.status_code != 200:
        raise Exception(response.url, response.text, details)
    return response.content


