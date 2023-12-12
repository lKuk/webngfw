from django.http import JsonResponse
from django.shortcuts import redirect, render

from ngfwadmin.views.debug.error import exception
from ngfwadmin.views.connect.connect import get_connect
from ngfwadmin.rest.write.write import get_write_in, get_write_out, get_write_content


def write(request):
    try:
        # Подключение
        dev = get_connect()
        # Проверка подключения
        if 'url' not in dev:
            return redirect('connect')

        # подключение
        url = dev.get('url')

        writeIn = get_write_in(url)
        writeOut = get_write_out(url)
        content = get_write_content(url)

        context = {'writeIn': writeIn,
                   'writeOut': writeOut,
                   'content': content
                   }
        # Вернуть данные
        ajax = request.GET.get("ajax")
        if ajax is not None:
            return JsonResponse(context)
        # Вернуть сформированную страницу
        return render(request, 'write/write.html', context=context)
    except Exception as ex:
        return exception(request, ex)
