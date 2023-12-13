from datetime import date

# подключения
dict_dev = {}


# Добавить подключение к устройству
def dev_set(request, ip, port, login, password):
    # время подключения
    now = date.today()
    # ссылка на устройство для rest
    url = 'http://' + ip + ':' + str(port)
    # Сохранить подключение
    dev = {'ip': ip,
           'port': port,
           'login': login,
           'password': password,
           'datetime': now,
           'url': url}
    # получить ключ сессию
    session_key = request.session.session_key
    # подключения
    global dict_dev
    # добавить для текущей сессии
    dict_dev[session_key] = dev


# Получить подключение к устройству
def dev_get(request):
    # подключения
    global dict_dev
    # удалить старые подключения
    for key in dict_dev:
        dev = dict_dev[key]
        date = dev.get('datetime')
        if date < date.today():
            del dict_dev[key]
    # получить ключ сессию
    session_key = request.session.session_key
    # получить устройство
    dev = dict_dev.get(session_key)
    if dev is None:
        dev = {}
    # вернуть устройство
    return dev
