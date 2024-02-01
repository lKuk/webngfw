import json
import requests


# Вход в систему
def auth_logon(url, login, password):
    response = requests.post(f"{url}/auth", auth=(login, password))
    if response.status_code == 401:
        return response.text
    if response.status_code != 200:
        raise Exception(response.url, response.text)
    return 'ok'

