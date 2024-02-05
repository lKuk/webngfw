from django.shortcuts import redirect, render

from ngfwadmin.rest.auth.permissions import permissions_get
from ngfwadmin.views.connect.dev import dev_get
from ngfwadmin.views.debug.error import exception
from ngfwadmin.rest.auth.auth import auth_users_get, auth_users_set


# Страница протокола arp
def permissions(request):
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

        # Запрос всех пользователей
        users = auth_users_get(url, login, password)
        # Запрос всех прав пользователей
        permissions = permissions_get(url, login, password)

         # данные страницы
        context = {'dev': dev,
                   'users': users,
                   'permissions': permissions}
        # Вернуть сформированную страницу
        return render(request, 'auth/permissions.html', context=context)
    except Exception as ex:
        return exception(request, ex)
