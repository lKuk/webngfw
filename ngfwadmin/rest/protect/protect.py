import json
import requests


def get_arp_protect(url, login, password):
    response = requests.get(f"{url}/router/arp/protect", auth=(login, password), verify=False)
    if response.status_code != 200:
        raise Exception(response.url, response.text)
    details = response.json()
    return details


def get_icmp_protect(url, login, password):
    response = requests.get(f"{url}/router/icmp/protect", auth=(login, password), verify=False)
    if response.status_code != 200:
        raise Exception(response.url, response.text)
    details = response.json()
    return details


def get_dhcp_snooping(url, login, password):
    response = requests.get(f"{url}/router/dhcp/snooping", auth=(login, password), verify=False)
    if response.status_code != 200:
        raise Exception(response.url, response.text)
    details = response.json()
    return details


# Установить статус arp
def set_arp(url, login, password, limits, ports, status):
    dic = {'limits': limits,
           'ports': ports,
           'status': status}
    sjson = json.dumps(dic)
    details = json.loads(sjson)
    response = requests.put(f"{url}/router/arp/protect", json=details, auth=(login, password), verify=False)
    if response.status_code != 200:
        raise Exception(response.url, response.text, details)
    return response.content

# Установить статус ipmp
def set_ipmp(url, login, password, limits, ports, status):
    dic = {'limits': limits,
           'ports': ports,
           'status': status}
    sjson = json.dumps(dic)
    details = json.loads(sjson)
    response = requests.put(f"{url}/router/icmp/protect", json=details, auth=(login, password), verify=False)
    code = response.status_code
    if response.status_code != 200:
        raise Exception(response.url, response.text, details)
    return response.content

def set_dhcp(url, login, password, status):
    dic = {'dhcp_snooping': status}
    sjson = json.dumps(dic)
    details = json.loads(sjson)
    response = requests.put(f"{url}/router/dhcp/snooping", json=details, auth=(login, password), verify=False)
    code = response.status_code
    if response.status_code != 200:
        raise Exception(response.url, response.text, details)
    return response.content
