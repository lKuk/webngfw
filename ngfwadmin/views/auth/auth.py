from django.shortcuts import redirect, render

from ngfwadmin.views.connect.dev import dev_get
from ngfwadmin.views.debug.error import exception
from ngfwadmin.rest.classification.classification import classification_get, classification_set


# Страница протокола arp
def auth(request):
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

         # Данные страницы
        context = {'dev': dev}
        # Вернуть сформированную страницу
        return render(request, 'auth/auth.html', context=context)
    except Exception as ex:
        return exception(request, ex)
