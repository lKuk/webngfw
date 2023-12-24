import requests


def ports_get(url):
    response = requests.get(f"{url}/ports")
    if response.status_code != 200:
        raise Exception(response.url, response.text)
    details = response.json()
    return details


def ports_avail_get(url):
    response = requests.get(f"{url}/ports/avail")
    if response.status_code != 200:
        raise Exception(response.url, response.text)
    details = response.json()
    return details


def get_mgmnt_stat(url):
    response = requests.get(f"{url}/system/monitoring/interfaces/mgmnt")
    if response.status_code != 200:
        raise Exception(response.url, response.text)
    details = response.json()
    return details