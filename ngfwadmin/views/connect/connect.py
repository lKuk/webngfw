from django.shortcuts import redirect, render

from ngfwadmin.forms import ConnectForm
from ngfwadmin.views.debug.error import exception
from ngfwadmin.views.connect.dev import dev_set, dev_del


# Страница подключения к устройству
def connect(request):
    try:
        # Удалить подключение
        dev_del(request)
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
                # Сохранить подключение
                dev_set(request, ip, port, login, password)
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
