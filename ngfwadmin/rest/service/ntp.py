import requests
import json

# Получение состояние клиента ntp
def ntp_status_get(url, login, password):
    response = requests.get(f"{url}/system/ntp/status", auth=(login, password), verify=False)
    if response.status_code != 200:
        raise Exception(response.url, response.text)
    details = response.json()
    return details

# Получение настроек клиента NTP
def ntp_server_get(url, login, password):
    response = requests.get(f"{url}/system/ntp/server", auth=(login, password), verify=False)
    if response.status_code != 200:
        raise Exception(response.url, response.text)
    details = response.json()
    return details