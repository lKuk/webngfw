import json
import requests


def get_syslog_server(url, login, password):
    response = requests.get(f"{url}/system/syslog/server", auth=(login, password))
    if response.status_code != 200:
        raise Exception(response.url, response.text)
    details = response.json()
    return details


def get_syslog_types(url, login, password):
    response = requests.get(f"{url}/system/syslog/types", auth=(login, password))
    if response.status_code != 200:
        raise Exception(response.url, response.text)
    details = response.json()
    return details


# Установить статус
def type_set(url, login, password, status, typesys):
    status = json.loads(status.lower())
    dic = {typesys: status}
    sjson = json.dumps(dic)
    details = json.loads(sjson)
    response = requests.put(f"{url}/system/syslog/types/{typesys}", json=details, auth=(login, password))
    if response.status_code != 200:
        raise Exception(response.url, response.text, details)
    return response.content

def server_set(url, login, password, ipServer, portServer):
    dic = {"port": portServer, "host": ipServer}
    sjson = json.dumps(dic)
    details = json.loads(sjson)
    response = requests.put(f"{url}/system/syslog/server", json=details, auth=(login, password))
    if response.status_code != 200:
        raise Exception(response.url, response.text, details)
    return response.content
