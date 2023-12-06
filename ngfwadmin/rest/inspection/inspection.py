import json
import requests



# Получить статус
def status_get(url):
    response = requests.get(f"{url}/inspection/status")
    if response.status_code != 200:
        raise Exception(response.url, response.text)
    details = response.json()
    return details


# Изменить список
def status_set(url, status):
    dic = {'tls_mitm_enable': status}
    sjson = json.dumps(dic)
    details = json.loads(sjson)
    response = requests.put(f"{url}/inspection/status", json=details)
    if response.status_code != 200:
        raise Exception(response.url, response.text, details)
    return response.content


def ca_get(url):
    response = requests.get(f"{url}/inspection/ca")
    if response.status_code != 200:
        raise Exception(response.url, response.text)
    details = response.json()
    return details

