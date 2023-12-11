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
    if 'message' in details:
        details = details['message']
        raise Exception(response.url, details)
    if 'cpu_workload' in details:
        details = details['cpu_workload']
    lcores = {}
    for index in range(len(details)):
        key = 'core_' + str(index)
        value = details[index]
        lcores[key] = value
    return lcores
