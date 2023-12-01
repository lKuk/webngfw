import requests


def monitoring_ram_get(url):
    response = requests.get(f"{url}/system/monitoring/ram")
    if response.status_code != 200:
        raise Exception(response.url, response.text)
    details = response.json()
    return details


def monitoring_disk_get(url):
    response = requests.get(f"{url}/system/monitoring/disk")
    if response.status_code != 200:
        raise Exception(response.url, response.text)
    details = response.json()
    return details


def monitoring_lcores_get(url):
    response = requests.get(f"{url}/system/monitoring/lcores")
    if response.status_code != 200:
        raise Exception(response.url, response.text)
    details = response.json()
    return details
