import json

import requests


# Получить arp таблицу
def dhcp_table_select(url):
    response = requests.get(f"{url}/router/dhcp/table")
    if response.status_code != 200:
        raise Exception(response.url, response.text)
    details = response.json()
    return details

def get_table_status(url):
    response = requests.get(f"{url}/router/dhcp/status")
    if response.status_code != 200:
        raise Exception(response.url, response.text)
    details = response.json()
    return details

# Установить параметры записи выходного трафика
def set_table_status(url, dhcp_enable):
    dic = {"dhcp_enable": dhcp_enable}
    sjson = json.dumps(dic)
    details = json.loads(sjson)
    response = requests.put(f"{url}/router/dhcp/status", json=details)
    if response.status_code != 200:
        raise Exception(response.url, response.text, details)
    return response.content



