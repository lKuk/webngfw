import json
import requests


# Восстановить правила из историю
def history_set(url, date):
    dic = {'date': date}
    sjson = json.dumps(dic)
    details = json.loads(sjson)
    response = requests.post(f"{url}/rules/history", json=details)
    if response.status_code != 200:
        raise Exception(response.url, response.text, details)
    return response.content


# Получить историю изменения правил
def history_get(url):
    response = requests.get(f"{url}/rules/history")
    if response.status_code != 200:
        raise Exception(response.url, response.text)
    details = response.json()
    return details
