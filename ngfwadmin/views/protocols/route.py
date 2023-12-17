
from django.shortcuts import redirect, render

from ngfwadmin.views.connect.dev import dev_get
from ngfwadmin.views.debug.error import exception
from ngfwadmin.rest.protocols.route import ip_router_delete, ip_router_select_all, ip_router_insert


# Страница протокола ip
def protocol_route(request):
    try:
        # Подключение
        dev = dev_get(request)
        # Проверка подключения
        if 'url' not in dev:
            return redirect('connect')
        # подключение
        url = dev.get('url')
        # удалить маршрут
        delete = request.GET.get("delete")
        if delete is not None:
            # удалить маршрут
            ip_router_delete(url, delete)
            # перейти к таблице списков
            return redirect('protocol_route')
        # Данные страницы
        route = ip_router_select_all(url)
        context = {'dev': dev,
                   'route': route}
        # Вернуть сформированную страницу
        return render(request, 'protocols/route/route.html', context=context)
    except Exception as ex:
        return exception(request, ex)


def protocol_route_add(request):
    try:
        # Подключение
        dev = dev_get(request)
        # Проверка подключения
        if 'url' not in dev:
            return redirect('connect')
        # подключение
        url = dev.get('url')
        # создать маршрут
        if request.method == 'POST':
            # добавить маршрут
            if 'btnInsert' in request.POST:
                # Получить параметры
                ip = request.POST.get('ip')
                mask = request.POST.get('mask')
                ipgw = request.POST.get('ipgw')
                # добавить маршрут
                ip_router_insert(url, ip, mask, ipgw)
                # перейти к таблице маршрутов
                return redirect('protocol_route')
        # Данные страницы
        context = {'dev': dev}
        # Вернуть сформированную страницу
        return render(request, 'protocols/route/route_form.html', context=context)
    except Exception as ex:
        return exception(request, ex)
