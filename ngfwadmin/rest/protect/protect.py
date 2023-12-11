import requests
import json


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
