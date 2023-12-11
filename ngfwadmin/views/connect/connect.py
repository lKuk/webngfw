from django.shortcuts import redirect, render

from ngfwadmin.forms import ConnectForm
from ngfwadmin.views.debug.error import exception


# устройство
device_connect = {}


# Подключение к устройству
def get_connect():
    # подключение к устройству
    global device_connect

    # Заполнить данные
    # device_connect = {'mode': 'local',
    #                   'ip': '192.168.3.250',
    #                   'port': '18888',
    #                   'login': 'admin',
    #                   'password': '111111',
    #                   'url': 'http://192.168.3.250:18888'}

    # вернуть подключение
    return device_connect


# Страница подключения к устройству
def connect(request):
    try:
        # подключение к устройству
        global device_connect

        # сбросить устройство
        device_connect = {}

        # Подключение
        if request.method == 'POST':
            form = ConnectForm(request.POST)
            # Проверка заполнения
            if form.is_valid():
                # данные формы
                obj = form.cleaned_data
                # Заполнить данные
                ip = obj['ip']
                port = obj['port']
                login = obj['login']
                password = obj['password']
                url = 'http://' + ip + ':' + str(port)
                # Сохранить подключение
                device_connect = {'ip': ip,
                                  'port': port,
                                  'login': login,
                                  'password': password,
                                  'url': url}
                # Подключение выполнено
                return redirect('state')
        # Подключение повторно
        else:
            form = ConnectForm()

        # Отобразить страницу подключения
        context = {'form': form}
        return render(request, 'connect/connect.html', context=context)

    except Exception as ex:
        return exception(request, ex)
