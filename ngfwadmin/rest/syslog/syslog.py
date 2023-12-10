import requests


def get_syslog_server(url):
    response = requests.get(f"{url}/system/syslog/server")
    if response.status_code != 200:
        raise Exception(response.url, response.text)
    details = response.json()
    return details


def get_syslog_types(url):
    response = requests.get(f"{url}/system/syslog/types")
    if response.status_code != 200:
        raise Exception(response.url, response.text)
    details = response.json()
    if 'Версия ПО' in details:
        details['version'] = details['Версия ПО']
    return details
