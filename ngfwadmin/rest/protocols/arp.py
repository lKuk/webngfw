import requests


# Получить arp таблицу
def arp_select(url, login, password):
    response = requests.get(f"{url}/router/arp/table", auth=(login, password), verify=False)
    if response.status_code != 200:
        raise Exception(response.url, response.text)
    details = response.json()
    return details


# Очистить arp таблицу
def arp_clear(url, login, password):
    response = requests.delete(f"{url}/router/arp/table", auth=(login, password), verify=False)
    if response.status_code != 200:
        raise Exception(response.url, response.text)
    return response.content
