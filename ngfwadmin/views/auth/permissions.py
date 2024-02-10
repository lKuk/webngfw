from django.shortcuts import redirect, render

from ngfwadmin.rest.auth.permissions import permissions_get, permissions_set
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

        # изменить состояние подсети
        path = request.GET.get("path")
        user = request.GET.get("user")
        permission = request.GET.get("permission")
        if path is not None and user is not None and permission is not None:
            permissions_set(url, login, password, path, user, permission)
            return

        # Запрос всех прав пользователей
        permissions = permissions_get(url, login, password)
        # Получить всех пользователей
        users = []
        for perm in permissions:
            for user in perm.get('permissions'):
                if user not in users:
                    users.append(user)

         # данные страницы
        context = {'dev': dev,
                   'users': users,
                   'permissions': permissions}
        # Вернуть сформированную страницу
        return render(request, 'auth/permissions.html', context=context)
    except Exception as ex:
        return exception(request, ex)
