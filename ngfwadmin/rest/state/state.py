import requests

# Получить версию
def version_get(url):
    response = requests.get(f"{url}/system/version")
    if response.status_code != 200:
        raise Exception(response.url, response.text)
    details = response.json()
    if 'Версия ПО' in details:
        details['version'] = details['Версия ПО']
    return details


# Получить версию
def serial_get(url):
    response = requests.get(f"{url}/system/serial")
    if response.status_code != 200:
        raise Exception(response.url, response.text)
    details = response.json()
    return details


# Получить статус
def status_get(url):
    response = requests.get(f"{url}/system/status")
    if response.status_code != 200:
        raise Exception(response.url, response.text)
    details = response.json()
    return details


# Получить статус
def uptime_get(url):
    response = requests.get(f"{url}/system/uptime")
    if response.status_code != 200:
        raise Exception(response.url, response.text)
    details = response.json()
    return details


# Получить статус
def sys_ports_get(url):
    response = requests.get(f"{url}/system/ports")
    if response.status_code != 200:
        raise Exception(response.url, response.text)
    details = response.json()
    return details


# Получить версию
def settings_get(url):
    response = requests.get(f"{url}/system/settings")
    if response.status_code != 200:
        raise Exception(response.url, response.text)
    details = response.json()
    return details


# Получить версию
def system_exit(url):
    response = requests.post(f"{url}/system/exit")
    if response.status_code != 200:
        raise Exception(response.url, response.text)
    details = response.json()
    return details
