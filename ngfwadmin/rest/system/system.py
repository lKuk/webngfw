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


# Получить версию
def lcores_get(url):
    response = requests.get(f"{url}/system/lcores")
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
