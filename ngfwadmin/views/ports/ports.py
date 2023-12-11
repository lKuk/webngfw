
from django.http import JsonResponse
from django.shortcuts import redirect, render

from ngfwadmin.rest.ports.ports import ports_get
from ngfwadmin.views.debug.error import exception
from ngfwadmin.views.connect.connect import get_connect


# Страница состояния портов
def ports(request):
    try:
        # Подключение
        dev = get_connect()
        # Проверка подключения
        if 'url' not in dev:
            return redirect('connect')
        # подключение
        url = dev.get('url')
        port = ports_get(url)
        context = {'dev': dev,
                   'ports': port}
        # Вернуть данные
        ajax = request.GET.get("ajax")
        if ajax is not None:
            return JsonResponse(context)
        # Вернуть сформированную страницу
        return render(request, 'ports/ports.html', context=context)
    except Exception as ex:
        return exception(request, ex)
