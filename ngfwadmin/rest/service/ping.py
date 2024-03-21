import requests
import json


# Отправить пинг
def ping_post(url, login, password,ipServer ,portServer, req_amount,delay):
    dic = {"ip_or_host": ipServer, "port": int(portServer), "req_amount": int(req_amount), "delay" : int(delay)}
    sjson = json.dumps(dic)
    details = json.loads(sjson)
    response = requests.post(f"{url}/service/ping", json=details, auth=(login, password), verify=False)
    # if response.status_code != 200:
    #     raise Exception(response.url, response.text, details)
    return response.content