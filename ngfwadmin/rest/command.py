import json
import requests


def command(url, login, password, val_command, val_connection):
    dic = {'command': val_command,
           'connection': val_connection,}
    sjson = json.dumps(dic)
    details = json.loads(sjson)
    response = requests.post(f"{url}/command", json=details, auth=(login, password), verify=False)
    if response.status_code != 200:
        raise Exception(response.url, response.text, details)
    return response.content
