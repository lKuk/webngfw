from django.shortcuts import redirect, render

from ngfwadmin.views.connect.dev import dev_get
from ngfwadmin.views.debug.error import exception
from ngfwadmin.rest.auth.auth import auth_users_get, auth_users_set


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

        # получить список пользователей
        users = auth_users_get(url, login, password)

         # данные страницы
        context = {'dev': dev,
                   'users': users}
        # Вернуть сформированную страницу
        return render(request, 'auth/auth.html', context=context)
    except Exception as ex:
        return exception(request, ex)


def auth_user(request, user):
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

        # изменить параметры пользователя
        if request.method == 'POST':
            if 'btnSet' in request.POST:
                # получить параметры
                pass1 = request.POST.get('pass1')
                pass2 = request.POST.get('pass2')
                if pass1 == pass2:
                    auth_users_set(url, login, password, user, pass1)
                    return redirect('auth')

         # данные страницы
        context = {'dev': dev,
                   'user': user}
        # Вернуть сформированную страницу
        return render(request, 'auth/auth_form.html', context=context)
    except Exception as ex:
        return exception(request, ex)