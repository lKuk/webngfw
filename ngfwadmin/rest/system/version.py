import requests

version = None


# Получить версию
def version_get(url):
    global version
    if version is not None:
        return version
    response = requests.get(f"{url}/system/version")
    if response.status_code != 200:
        raise Exception(response.url, response.text)
    version = response.json()
    version = version['Версия ПО']
    return version
