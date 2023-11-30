from ngfwadmin.forms import *
from ngfwadmin.views.debug.debug import exception

from django.shortcuts import redirect, render


# устройство
device_connect = {}


# Подключение к устройству
def get_connect():
    global device_connect
    # device_connect = {'mode': 'local',
    #                   'ip': '192.168.3.250',
    #                   'port': '18888',
    #                   'login': 'admin',
    #                   'password': '111111',
    #                   'url': 'http://192.168.3.250:18888'}
    return device_connect


# Страница подключения к устройству
def connect(request):
    try:
        if request.method == 'POST':
            form = ConnectForm(request.POST)
            if form.is_valid():
                obj = form.cleaned_data
                global device_connect
                ip = obj['ip']
                port = obj['port']
                login = obj['login']
                password = obj['password']
                url = 'http://' + ip + ':' + str(port)
                device_connect = {'ip': ip,
                                  'port': port,
                                  'login': login,
                                  'password': password,
                                  'url': url}
                return redirect('ngfwsys')
        else:
            form = ConnectForm()
        context = {'form': form}
        return render(request, 'connect/connect.html', context=context)
    except Exception as ex:
        return exception(request, ex)
