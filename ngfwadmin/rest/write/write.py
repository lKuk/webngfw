import requests
import json


def get_write_in(url):
    response = requests.get(f"{url}/system/service/write/in")
    if response.status_code != 200:
        raise Exception(response.url, response.text)
    details = response.json()
    return details


def get_write_out(url):
    response = requests.get(f"{url}/system/service/write/out")
    if response.status_code != 200:
        raise Exception(response.url, response.text)
    details = response.json()
    return details


def get_write_content(url):
    response = requests.get(f"{url}/system/service/write/content")
    if response.status_code != 200:
        raise Exception(response.url, response.text)
    details = response.json()
    return details
