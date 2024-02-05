import json
import requests


# kполучить таблицу всех прав всех пользователей
def permissions_get(url, login, password):
    response = requests.get(f"{url}/auth/permissions", auth=(login, password), verify=False)
    if response.status_code != 200:
        raise Exception(response.url, response.text)
    details = response.json()

    details = json.loads('''
    [
        {
          "path": "/auth",
          "name": "Пароли пользователей",
          "permissions": { "administrator": "READONLY", "user": "NONE", "ibadmin": "READWRITE" }
        },
        {
          "path": "/auth/permissions",
          "name": "Привилегии пользователей",
          "permissions": { "administrator": "READWRITE", "user": "NONE", "ibadmin": "READWRITE" }
        },
        {
          "path": "/system",
          "name": "Состояние системы",
          "permissions": { "administrator": "READONLY", "user": "READONLY", "ibadmin": "READWRITE" }
        },
        {
          "path": "/rules",
          "name": "Правила фильтрации",
          "permissions": { "administrator": "READWRITE", "user": "READWRITE", "ibadmin": "READWRITE" }
        }
    ]
    ''')

    return details