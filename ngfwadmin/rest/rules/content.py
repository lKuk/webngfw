import requests


# Установить содержимое списка
def content_set(url, login, password, idlist, filetext):
    response = requests.put(f"{url}/rules/lists/{idlist}/content", data=filetext, auth=(login, password))
    if response.status_code != 200:
        raise Exception(response.url, response.text)
    return response.content


# Получить содержимое списка
def content_get(url, idlist):
    response = requests.get(f"{url}/rules/lists/{idlist}/content")
    if response.status_code != 200:
        return ''
    details = response.text
    return details

