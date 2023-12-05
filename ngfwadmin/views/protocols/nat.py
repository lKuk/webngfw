
from django.shortcuts import redirect, render

from ngfwadmin.views.debug.error import exception
from ngfwadmin.views.connect.connect import get_connect


# Страница протокола nat
def protocol_nat(request):
    try:
        # Подключение
        dev = get_connect()
        # Проверка подключения
        if 'url' not in dev:
            return redirect('connect')
        # подключение
        url = dev.get('url')
        # Данные страницы
        context = {'dev': dev}
        # Вернуть сформированную страницу
        return render(request, 'protocols/nat.html', context=context)
    except Exception as ex:
        return exception(request, ex)
