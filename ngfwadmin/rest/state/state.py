import requests


# Получить версию
def version_get(url, login, password):
    response = requests.get(f"{url}/system/version", auth=(login, password), verify=False)
    if response.status_code != 200:
        raise Exception(response.url, response.text)
    details = response.json()
    if 'Версия ПО' in details:
        details['version'] = details['Версия ПО']
    return details


# Получить версию
def serial_get(url, login, password):
    response = requests.get(f"{url}/system/serial", auth=(login, password), verify=False)
    if response.status_code != 200:
        raise Exception(response.url, response.text)
    details = response.json()
    return details


# Получить статус
def status_get(url, login, password):
    response = requests.get(f"{url}/system/status", auth=(login, password), verify=False)
    if response.status_code != 200:
        raise Exception(response.url, response.text)
    details = response.json()
    return details


# Получить статус
def uptime_get(url, login, password):
    response = requests.get(f"{url}/system/uptime", auth=(login, password), verify=False)
    if response.status_code != 200:
        raise Exception(response.url, response.text)
    details = response.json()
    return details


# Получить статус
def sys_ports_get(url, login, password):
    response = requests.get(f"{url}/system/ports", auth=(login, password), verify=False)
    if response.status_code != 200:
        raise Exception(response.url, response.text)
    details = response.json()
    return details


# Получить версию
def settings_get(url, login, password):
    response = requests.get(f"{url}/system/settings", auth=(login, password), verify=False)
    if response.status_code != 200:
        raise Exception(response.url, response.text)
    details = response.json()
    return details


# Получить версию
def system_exit(url, login, password):
    response = requests.post(f"{url}/system/exit", auth=(login, password), verify=False)
    if response.status_code != 200:
        raise Exception(response.url, response.text)
    details = response.json()
    return details
