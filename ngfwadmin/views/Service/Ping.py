
from django.shortcuts import redirect, render

from ngfwadmin.views.connect.dev import dev_get
from ngfwadmin.views.debug.error import exception
from ngfwadmin.rest.protocols.arp import arp_select, arp_clear

# Страница протокола arp
def ping(request):
    try:
        # Подключение
        dev = dev_get(request)
        # Проверка подключения
        if 'url' not in dev or 'login' not in dev or 'password' not in dev:
            return redirect('connect')
        # подключение
        url = dev.get('url')
        login = dev.get('login')
        password = dev.get('password')
        # Получить arp таблицу
        arp = arp_select(url, login, password)

        # создать список
        if request.method == 'POST':
            # добавить список
            if 'btnClear' in request.POST:
                # Очистить arp таблицу
                arp_clear(url, login, password)

        # Данные страницы
        context = {'dev': dev,
                   'arp': arp,
                   }
        # Вернуть сформированную страницу
        return render(request, 'Service/ping.html', context=context)
    except Exception as ex:
        return exception(request, ex)
