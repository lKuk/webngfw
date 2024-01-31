import json
import requests



# Получить параметры записи входного трафика
def get_write_in(url, login, password):
    response = requests.get(f"{url}/system/service/write/in", auth=(login, password))
    if response.status_code != 200:
        raise Exception(response.url, response.text)
    details = response.json()
    return details


# Установить параметры записи входного трафика
def set_write_in(url, write_portin, write_statusin):
    dic = {"write_portin": write_portin, "write_statusin": write_statusin}
    sjson = json.dumps(dic)
    details = json.loads(sjson)
    response = requests.put(f"{url}/system/service/write/in", json=details, auth=(login, password))
    if response.status_code != 200:
        raise Exception(response.url, response.text, details)
    return response.content


# Получить параметры записи выходного трафика
def get_write_out(url, login, password):
    response = requests.get(f"{url}/system/service/write/out", auth=(login, password))
    if response.status_code != 200:
        raise Exception(response.url, response.text)
    details = response.json()
    return details


# Установить параметры записи выходного трафика
def set_write_out(url, port, protocol, write_statusout):
    dic = {"write_portout": port, "write_protout": protocol, "write_statusout": write_statusout}
    sjson = json.dumps(dic)
    details = json.loads(sjson)
    response = requests.put(f"{url}/system/service/write/out", json=details, auth=(login, password))
    if response.status_code != 200:
        raise Exception(response.url, response.text, details)
    return response.content


# Получить таблицу записанных файлов
def get_write_content(url, login, password):
    response = requests.get(f"{url}/system/service/write/content", auth=(login, password))
    if response.status_code != 200:
        raise Exception(response.url, response.text)
    details = response.json()
    return details


# Получить содержимое файла
def get_write_content_file(url, fileName):
    response = requests.get(f"{url}/system/service/write/content/{fileName}", auth=(login, password))
    if response.status_code != 200:
        raise Exception(response.url, response.text)
    details = response.text
    return details


# Удалить файл
def delete_write_content_file(url, fileName):
    response = requests.delete(f"{url}/system/service/write/content/{fileName}", auth=(login, password))
    if response.status_code != 200:
        raise Exception(response.url, response.text)
    details = response.text
    return details
