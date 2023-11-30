from ngfwadmin.forms import *
from django.shortcuts import redirect, render
from ngfwadmin.views.debug.debug import exception

# устройство
dev = {}
# dev = {'mode': 'local',
#        'ip':'192.168.3.250',
#        'port':'18888',
#        'login':'admin',
#        'password':'111111',
#        'url':'http://192.168.3.250:18888'}


# Страница подключения к устройству
def connect(request):
    try:
        if request.method == 'POST':
            form = ConnectForm(request.POST)
            if form.is_valid():
                obj = form.cleaned_data
                global dev
                ip = obj['ip']
                port = obj['port']
                login = obj['login']
                password = obj['password']
                url = 'http://' + ip + ':' + str(port)
                dev = {'ip': ip,
                       'port': port,
                       'login': login,
                       'password': password,
                       'url': url}
                return redirect('system')
        else:
            form = ConnectForm()
        context = {'form': form}
        return render(request, 'connect/connect.html', context=context)
    except Exception as ex:
        return exception(request, ex)
