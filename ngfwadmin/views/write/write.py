from django.http import JsonResponse, HttpResponse
from django.shortcuts import redirect, render

from ngfwadmin.views.connect.dev import dev_get
from ngfwadmin.views.debug.error import exception
from ngfwadmin.rest.write.write import get_write_in, get_write_out, set_write_in, set_write_out
from ngfwadmin.rest.write.write import get_write_content, get_write_content_file, delete_write_content_file


def write(request):
    try:
        # Подключение
        dev = dev_get(request)
        # Проверка подключения
        if 'url' not in dev:
            return redirect('connect')

        # подключение
        url = dev.get('url')

        # получить данные
        writeIn = get_write_in(url)
        writeOut = get_write_out(url)
        writeContent = get_write_content(url)

        # начать/остановить запись
        port = request.GET.get("port")
        param = request.GET.get("param")
        status = request.GET.get("status")
        if param is not None and status is not None and port is not None:
            # начать запись вх.
            if param == 'In' and status != 'write':
                set_write_in(url, port, 'write')
            # начать запись исх.
            elif param == 'Out' and status != 'write':
                set_write_out(url, port, 'write')
            # остановить запись вх.
            elif param == 'In' and status == 'write':
                set_write_in(url, writeIn['write_portin'], 'stop')
            # остановить запись исх.
            elif param == 'Out' and status == 'write':
                set_write_out(url, writeOut['write_portout'], 'stop')
            return

        # скачать файл
        pcap = request.GET.get('pcap')
        if pcap is not None:
            file = get_write_content_file(url, pcap)
            return HttpResponse(file)

        # удалить файл
        delete = request.GET.get("delete")
        if delete is not None:
            delete_write_content_file(url, delete)
            return redirect('write')

        # заполнить данные
        context = {'dev': dev,
                   'writeIn': writeIn,
                   'writeOut': writeOut,
                   'writeContent': writeContent}

        # Вернуть данные
        ajax = request.GET.get("ajax")
        if ajax is not None:
            return JsonResponse(context)

        # Вернуть сформированную страницу
        return render(request, 'write/write.html', context=context)
    except Exception as ex:
        return exception(request, ex)
