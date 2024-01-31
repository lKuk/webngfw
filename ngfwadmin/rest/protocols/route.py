import json
import requests


# Добавить список
def ip_router_insert(url, login, password, ip, mask, ipgw):
    if ipgw is None or ipgw.strip() == '':
        ipgw = '-'
    dic = {
        'ip': str(ip),
        'mask': str(mask),
        'ipgw': str(ipgw)}
    sjson = json.dumps(dic)
    details = json.loads(sjson)
    response = requests.post(f"{url}/router/ip/route", json=details, auth=(login, password))
    if response.status_code != 200:
        raise Exception(response.url, response.text, details)
    return response.content


# Удалить список
def ip_router_delete(url, login, password, id):
    dic = {'ind': id}
    sjson = json.dumps(dic)
    details = json.loads(sjson)
    response = requests.delete(f"{url}/router/ip/route", json=details, auth=(login, password))
    if response.status_code != 200:
        raise Exception(response.url, response.text)
    return response.content


# Получить все списки
def ip_router_select_all(url, login, password):
    response = requests.get(f"{url}/router/ip/route", auth=(login, password))
    if response.status_code != 200:
        raise Exception(response.url, response.text)
    details = response.json()
    return details
