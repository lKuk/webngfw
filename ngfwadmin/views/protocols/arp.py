
from django.shortcuts import redirect, render

from ngfwadmin.views.debug.error import exception
from ngfwadmin.views.connect.connect import get_connect
from ngfwadmin.rest.protocols.arp import arp_select, arp_clear


# Страница протокола arp
def protocol_arp(request):
    try:
        # Подключение
        dev = get_connect()
        # Проверка подключения
        if 'url' not in dev:
            return redirect('connect')
        # подключение
        url = dev.get('url')
        # Получить arp таблицу
        arp = arp_select(url)

        # создать список
        if request.method == 'POST':
            # добавить список
            if 'btnClear' in request.POST:
                # Очистить arp таблицу
                arp_clear(url)

        # Данные страницы
        context = {'dev': dev,
                   'arp': arp }
        # Вернуть сформированную страницу
        return render(request, 'protocols/arp.html', context=context)
    except Exception as ex:
        return exception(request, ex)
