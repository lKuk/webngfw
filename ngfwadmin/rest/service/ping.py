import requests
import json


# Отправить пинг
def set_write_out(url, login, password, port, protocol, write_statusout):
    dic = {"write_portout": port, "write_protout": protocol, "write_statusout": write_statusout}
    sjson = json.dumps(dic)
    details = json.loads(sjson)
    # response = requests.put(f"{url}/system/service/write/out", json=details, auth=(login, password), verify=False)
    response = requests.put(f"{url}/service/write/out", json=details, auth=(login, password), verify=False)
    if response.status_code != 200:
        raise Exception(response.url, response.text, details)
    return response.content