import json
import requests


# Добавить список
def ipconfig_insert(url, ip, mask, vlan, port, ipgw):
    dic = {
        'ip': str(ip),
        'mask': str(mask),
        'port': str(port),
        'ipgw': str(ipgw),
        'vlan_id': str(vlan)}
    sjson = json.dumps(dic)
    details = json.loads(sjson)
    response = requests.post(f"{url}/router/ip/config", json=details)
    if response.status_code != 200:
        raise Exception(response.url, response.text, details)
    return response.content


# Удалить список
def ipconfig_delete(url, id, port):
    dic = {'id': id,
           'port': port }
    sjson = json.dumps(dic)
    details = json.loads(sjson)
    response = requests.delete(f"{url}/router/ip/config", json=details)
    if response.status_code != 200:
        raise Exception(response.url, response.text)
    return response.content


# Получить все списки
def ipconfig_select_all(url):
    response = requests.get(f"{url}/router/ip/config")
    if response.status_code != 200:
        raise Exception(response.url, response.text)
    details = response.json()
    return details
