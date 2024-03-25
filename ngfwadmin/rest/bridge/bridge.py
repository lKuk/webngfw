import json
import requests


def get_bridge(url, login, password):
    # response = requests.get(f"{url}/router/arp/protect", auth=(login, password), verify=False)
    response = requests.get(f"{url}/router/mode", auth=(login, password), verify=False)
    if response.status_code != 200:
        raise Exception(response.url, response.text)
    details = response.json()
    return details


# Установить статус arp
def set_bridge(url, login, password, status):
    if status == "true":
        status = True
    else:
        status = False
    dic = {'l2': status}
    sjson = json.dumps(dic)
    details = json.loads(sjson)
    response = requests.put(f"{url}/router/mode", json=details, auth=(login, password), verify=False)
    if response.status_code != 200:
        raise Exception(response.url, response.text, details)
    return response.content


