import requests


enum_mimes = None
enum_atomic = None
enum_format = None
enum_services = None
enum_protocols = None
enum_format_ftype = None


# Получить атомарные правила
def enum_atomic_get(url):
    global enum_atomic
    if enum_atomic is not None:
        return enum_atomic
    response = requests.get(f"{url}/rules/atomic")
    if response.status_code != 200:
        raise Exception(response.url, response.text)
    data = response.json()
    enum_atomic = {}
    for ar in data['rules']:
        enum_atomic[ar['id']] = ar
    return enum_atomic


# Получить форматы атомарных правил
def enum_format_get(url):
    global enum_format
    if enum_format is not None:
        return enum_format
    response = requests.get(f"{url}/rules/atomic/format")
    if response.status_code != 200:
        raise Exception(response.url, response.text)
    enum_format = response.json()
    return enum_format


# Получить список сервисов
def enum_services_get(url):
    global enum_services
    if enum_services is not None:
        return enum_services
    response = requests.get(f"{url}/rules/lists/services")
    if response.status_code != 200:
        raise Exception(response.url, response.text)
    enum_services = response.json()
    return enum_services


# Получить список протоколов
def enum_protocols_get(url):
    global enum_protocols
    if enum_protocols is not None:
        return enum_protocols
    response = requests.get(f"{url}/rules/lists/protocols")
    if response.status_code != 200:
        raise Exception(response.url, response.text)
    enum_protocols = response.json()
    return enum_protocols


# Получить список mime
def enum_mimes_get(url):
    global enum_mimes
    if enum_mimes is not None:
        return enum_mimes
    response = requests.get(f"{url}/rules/lists/mimes")
    if response.status_code != 200:
        raise Exception(response.url, response.text)
    enum_mimes = response.json()
    return enum_mimes
