import json
import requests


def classification_get(url, login, password):
    response = requests.get(f"{url}/classification/status", auth=(login, password), verify=False)
    if response.status_code != 200:
        raise Exception(response.url, response.text)
    details = response.json()
    return details


def classification_set(url, login, password, cert_enable, signature_enable, service_class_enable, class_enable):
    dic = {"cert_enable": cert_enable, "signature_enable": signature_enable, "service_class_enable": service_class_enable,
           "class_enable": class_enable}
    sjson = json.dumps(dic)
    details = json.loads(sjson)
    response = requests.put(f"{url}/classification/status", json=details, auth=(login, password), verify=False)
    if response.status_code != 200:
        raise Exception(response.url, response.text, details)
    return response.content
