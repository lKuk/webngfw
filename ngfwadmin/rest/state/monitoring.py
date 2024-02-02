import requests


def monitoring_ram_get(url, login, password):
    response = requests.get(f"{url}/system/monitoring/ram", auth=(login, password), verify=False)
    if response.status_code != 200:
        raise Exception(response.url, response.text)
    details = response.json()
    return details


def monitoring_disk_get(url, login, password):
    response = requests.get(f"{url}/system/monitoring/disk", auth=(login, password), verify=False)
    if response.status_code != 200:
        raise Exception(response.url, response.text)
    details = response.json()
    return details

def monitoring_lcores_get(url, login, password):
    response = requests.get(f"{url}/system/monitoring/lcores", auth=(login, password), verify=False)
    if response.status_code != 200:
        raise Exception(response.url, response.text)
    details = response.json()
    if 'message' in details:
        details = details['message']
        raise Exception(response.url, details)
    return details
