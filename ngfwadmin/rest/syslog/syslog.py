import requests

def get_syslog_server(url):
    response = requests.get(f"{url}/system/syslog/server")
    if response.status_code != 200:
        raise Exception(response.url, response.text)
    details = response.json()
    return details