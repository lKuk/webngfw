import json
import requests


# Получить статус
def status_get(url, login, password):
    response = requests.get(f"{url}/inspection/status", auth=(login, password), verify=False)
    if response.status_code != 200:
        raise Exception(response.url, response.text)
    details = response.json()
    return details


# Изменить список
def status_set(url, login, password, status):
    dic = {'tls_mitm_enable': status}
    sjson = json.dumps(dic)
    details = json.loads(sjson)
    response = requests.put(f"{url}/inspection/status", json=details, auth=(login, password), verify=False)
    if response.status_code != 200:
        raise Exception(response.url, response.text, details)
    return response.content


# Получить сертификаты
def ca_get(url, login, password):
    response = requests.get(f"{url}/inspection/ca", auth=(login, password), verify=False)
    if response.status_code != 200:
        raise Exception(response.url, response.text)
    details = response.json()
    return details


# Установить сертификаты
def ca_set(url, login, password, key, cer):
    dic = {'key': key, 'cer': cer}
    sjson = json.dumps(dic)
    details = json.loads(sjson)
    response = requests.put(f"{url}/inspection/ca", json=details, auth=(login, password), verify=False)
    if response.status_code != 200:
        raise Exception(response.url, response.text, details)
    return response.content
