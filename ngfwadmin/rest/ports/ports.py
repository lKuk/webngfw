import requests


def ports_get(url, login, password):
    response = requests.get(f"{url}/ports", auth=(login, password), verify=False)
    if response.status_code != 200:
        raise Exception(response.url, response.text)
    details = response.json()
    return details


def ports_avail_get(url, login, password):
    response = requests.get(f"{url}/ports/avail", auth=(login, password), verify=False)
    if response.status_code != 200:
        raise Exception(response.url, response.text)
    details = response.json()
    return details


def get_mgmnt_stat(url, login, password):
    # response = requests.get(f"{url}/system/monitoring/interfaces/mgmnt", auth=(login, password), verify=False)
    response = requests.get(f"{url}/ports/internal/mgmnt", auth=(login, password), verify=False)
    if response.status_code != 200:
        raise Exception(response.url, response.text)
    details = response.json()
    return details

def get_graylog_stat(url, login, password):
    # response = requests.get(f"{url}/system/monitoring/interfaces/graylog", auth=(login, password), verify=False)
    response = requests.get(f"{url}/ports/internal/graylog", auth=(login, password), verify=False)
    if response.status_code != 200:
        raise Exception(response.url, response.text)
    details = response.json()
    return details