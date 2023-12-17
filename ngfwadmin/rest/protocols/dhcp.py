import json

import requests


# Получить dhcp таблицу
def dhcp_table_select(url):
    response = requests.get(f"{url}/router/dhcp/table")
    if response.status_code != 200:
        raise Exception(response.url, response.text)
    details = response.json()
    return details


# Получить статус dhcp
def get_table_status(url):
    response = requests.get(f"{url}/router/dhcp/status")
    if response.status_code != 200:
        raise Exception(response.url, response.text)
    details = response.json()
    return details


# Установить статус dhcp
def set_table_status(url, dhcp_enable):
    dic = {"dhcp_enable": dhcp_enable}
    sjson = json.dumps(dic)
    details = json.loads(sjson)
    response = requests.put(f"{url}/router/dhcp/status", json=details)
    if response.status_code != 200:
        raise Exception(response.url, response.text, details)
    return response.content


# Получить таблицу подсетей
def dhcp_subnet_select(url):
    response = requests.get(f"{url}/router/dhcp/subnet/table")
    if response.status_code != 200:
        raise Exception(response.url, response.text)
    details = response.json()
    return details


# Добавить запись в таблицу подсетей
def dhcp_subnet_insert(url, port, vlan, ip_start, ip_end, status):
    # задать диапазон
    scope = {"port": port,
             "vlan": vlan,
             "ip_end": ip_end,
             "ip_start": ip_start}
    response1 = requests.post(f"{url}/router/dhcp/subnet/scope", json=scope)
    if response1.status_code != 200:
        raise Exception(response1.url, response1.text, scope)
    # задать состояние
    port_vlan = {"port": port,
                 "vlan": vlan}
    if status == True:
        response2 = requests.delete(f"{url}/router/dhcp/subnet/status", json=port_vlan)
    else:
        response2 = requests.post(f"{url}/router/dhcp/subnet/status", json=port_vlan)
    if response2.status_code != 200:
        raise Exception(response2.url, response2.text)
    return


# Удалить запись в таблице подсетей
def dhcp_subnet_delete(url, port, vlan, ip_start, ip_end):
    details = {"port": port,
               "vlan": vlan,
               "ip_end": ip_end,
               "ip_start": ip_start}
    response = requests.delete(f"{url}/router/dhcp/subnet/scope", json=details)
    if response.status_code != 200:
        raise Exception(response.url, response.text)
    return
