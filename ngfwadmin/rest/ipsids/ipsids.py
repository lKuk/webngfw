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


# Установить правила
def rules_set(url, filetext):
    response = requests.put(f"{url}/ipsids/rules", data=filetext)
    if response.status_code != 200:
        raise Exception(response.url, response.text)
    return response.content


# Получить конфигурацию
def configuration_get(url):
    response = requests.get(f"{url}/ipsids/configuration")
    if response.status_code != 200:
        raise Exception(response.url, response.text)
    details = response.text
    return details


# Установить конфигурацию
def configuration_set(url, filetext):
    response = requests.put(f"{url}/ipsids/configuration", data=filetext)
    if response.status_code != 200:
        raise Exception(response.url, response.text)
    return response.content
