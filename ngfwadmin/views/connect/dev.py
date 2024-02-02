from datetime import date

# подключения
dict_dev = {}


# Добавить подключение к устройству
def dev_set(request, ip, port, login, password):
    # время подключения
    now = date.today()
    # ссылка на устройство для rest
    url = get_url(ip, port)
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


# Добавить подключение к устройству
def get_url(ip, port):
    return 'https://' + ip + ':' + str(port)

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


# Удалить подключение к устройству
def dev_del(request):
    # подключения
    global dict_dev
    # получить ключ сессию
    session_key = request.session.session_key
    # удалить устройство
    if session_key in dict_dev:
        del dict_dev[session_key]