import requests
import json


def get_syslog_server(url):
    response = requests.get(f"{url}/system/syslog/server")
    if response.status_code != 200:
        raise Exception(response.url, response.text)
    details = response.json()
    return details


def get_syslog_types(url):
    response = requests.get(f"{url}/system/syslog/types")
    if response.status_code != 200:
        raise Exception(response.url, response.text)
    details = response.json()
    return details


# Установить статус
def type_set(url, status, typesys):
    status = json.loads(status.lower())
    dic = {typesys: status}
    sjson = json.dumps(dic)
    details = json.loads(sjson)
    response = requests.put(f"{url}/system/syslog/types/{typesys}", json=details)
    if response.status_code != 200:
        raise Exception(response.url, response.text, details)
    return response.content

def server_set(url, ipServer, portServer):
    dic = {"port": portServer, "host": ipServer}
    sjson = json.dumps(dic)
    details = json.loads(sjson)
    response = requests.put(f"{url}/system/syslog/server", json=details)
    if response.status_code != 200:
        raise Exception(response.url, response.text, details)
    return response.content
