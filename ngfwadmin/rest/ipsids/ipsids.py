import json
import requests


# Получить статус
def status_get(url, login, password):
    response = requests.get(f"{url}/ipsids/status", auth=(login, password))
    if response.status_code != 200:
        raise Exception(response.url, response.text)
    details = response.json()
    return details


# Установить статус
def status_set(url, login, password, status):
    dic = {'ipsids_enable': status}
    sjson = json.dumps(dic)
    details = json.loads(sjson)
    response = requests.put(f"{url}/ipsids/status", json=details, auth=(login, password))
    if response.status_code != 200:
        raise Exception(response.url, response.text, details)
    return response.content


# Получить правила
def rules_get(url, login, password):
    response = requests.get(f"{url}/ipsids/rules", auth=(login, password))
    if response.status_code != 200:
        raise Exception(response.url, response.text)
    details = response.text
    return details


# Установить правила
def rules_set(url, login, password, filetext):
    buffer = bytes(filetext, 'utf-8')
    response = requests.put(f"{url}/ipsids/rules", data=buffer, auth=(login, password))
    if response.status_code != 200:
        raise Exception(response.url, response.text)
    return response.content


# Получить конфигурацию
def configuration_get(url, login, password):
    response = requests.get(f"{url}/ipsids/configuration", auth=(login, password))
    if response.status_code != 200:
        raise Exception(response.url, response.text)
    details = response.text
    return details


# Установить конфигурацию
def configuration_set(url, login, password, filetext):
    buffer = bytes(filetext, 'utf-8')
    response = requests.put(f"{url}/ipsids/configuration", data=buffer, auth=(login, password))
    if response.status_code != 200:
        raise Exception(response.url, response.text)
    return response.content
