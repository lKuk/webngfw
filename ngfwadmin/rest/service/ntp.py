import requests
import json

# Получение состояние клиента ntp
def ntp_status_get(url, login, password):
    response = requests.get(f"{url}/system/ntp/status", auth=(login, password), verify=False)
    if response.status_code != 200:
        raise Exception(response.url, response.text)
    details = response.json()
    return details

# Получение настроек клиента NTP
def ntp_server_get(url, login, password):
    response = requests.get(f"{url}/system/ntp/server", auth=(login, password), verify=False)
    if response.status_code != 200:
        raise Exception(response.url, response.text)
    details = response.json()
    return details


# Добавить правило
def ntp_server_add(url, login, password, ip, prefer):
    if prefer == 'false':
        prefer = False
    else:
        prefer = True
    dic = {
        'ip': ip,
        'prefer': prefer}
    sjson = json.dumps(dic)
    details = json.loads(sjson)
    response = requests.post(f"{url}/system/ntp/server", json=details, auth=(login, password), verify=False)
    if response.status_code != 200:
        raise Exception(response.url, response.text, details)
    return response.content


# Удалить сереп
def ntp_server_delete(url, login, password, ip):
    dic = {
        'ip': ip,
    }
    sjson = json.dumps(dic)
    details = json.loads(sjson)
    response = requests.delete(f"{url}/system/ntp/server", json=details, auth=(login, password), verify=False)
    if response.status_code != 200:
        raise Exception(response.url, response.text)
    return response.content