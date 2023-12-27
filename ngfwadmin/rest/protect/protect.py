import json
import requests


def get_arp_protect(url):
    response = requests.get(f"{url}/router/arp/protect")
    if response.status_code != 200:
        raise Exception(response.url, response.text)
    details = response.json()
    return details


def get_icmp_protect(url):
    response = requests.get(f"{url}/router/icmp/protect")
    if response.status_code != 200:
        raise Exception(response.url, response.text)
    details = response.json()
    return details


def get_dhcp_snooping(url):
    response = requests.get(f"{url}/router/dhcp/snooping")
    if response.status_code != 200:
        raise Exception(response.url, response.text)
    details = response.json()
    return details


# Установить статус arp
def set_arp(url, limits, ports, status):
    dic = {'limits': limits,
           'ports': ports,
           'status': status}
    sjson = json.dumps(dic)
    details = json.loads(sjson)
    response = requests.put(f"{url}/router/arp/protect", json=details)
    if response.status_code != 200:
        raise Exception(response.url, response.text, details)
    return response.content

# Установить статус ipmp
def set_ipmp(url, limits, ports, status):
    dic = {'limits': limits,
           'ports': ports,
           'status': status}
    sjson = json.dumps(dic)
    details = json.loads(sjson)
    response = requests.put(f"{url}/router/icmp/protect", json=details)
    code = response.status_code
    if response.status_code != 200:
        raise Exception(response.url, response.text, details)
    return response.content

def set_dhcp(url, status):
    dic = {'dhcp_snooping': status}
    sjson = json.dumps(dic)
    details = json.loads(sjson)
    response = requests.put(f"{url}/router/dhcp/snooping", json=details)
    code = response.status_code
    if response.status_code != 200:
        raise Exception(response.url, response.text, details)
    return response.content
