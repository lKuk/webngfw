import requests


# Установить содержимое списка
def content_set(url, idlist, filetext):
    response = requests.put(f"{url}/rules/lists/{idlist}/content", data=filetext)
    if response.status_code != 200:
        raise Exception(response.url, response.text)
    return response.content


# Получить содержимое списка
def content_get(url, idlist):
    response = requests.get(f"{url}/rules/lists/{idlist}/content")
    if response.status_code != 200:
        raise Exception(response.url, response.text)
    details = response.text
    return details

