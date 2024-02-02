import base64
from io import BytesIO

from django.http import JsonResponse, HttpResponse, FileResponse
from django.shortcuts import redirect, render
from django.template.loader import render_to_string

from ngfwadmin.rest.rules.enum import enum_protocols_get, enum_services_get
from ngfwadmin.views.connect.dev import dev_get
from ngfwadmin.views.debug.error import exception
from ngfwadmin.rest.write.write import get_write_in, get_write_out, set_write_in, set_write_out
from ngfwadmin.rest.write.write import get_write_content, get_write_content_file, delete_write_content_file


def write(request):
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

        # получить данные
        writeIn = get_write_in(url, login, password)
        writeOut = get_write_out(url, login, password)

        # начать/остановить записьф
        port = request.GET.get("port")
        param = request.GET.get("param")
        status = request.GET.get("status")
        protocol = request.GET.get("protocol")
        if param is not None and status is not None and port is not None:
            # начать запись вх.
            if param == 'In' and status != 'write':
                set_write_in(url, login, password, port, 'write')
            # начать запись исх.
            elif param == 'Out' and status != 'write':
                set_write_out(url, login, password, port, protocol, 'write')
            # остановить запись вх.
            elif param == 'In' and status == 'write':
                set_write_in(url, login, password, writeIn['write_portin'], 'stop')
            # остановить запись исх.
            elif param == 'Out' and status == 'write':
                set_write_out(url, login, password, writeOut['write_portout'], writeOut['write_protout'], 'stop')
            return

        # удалить файл
        delete = request.GET.get("delete")
        if delete is not None:
            delete_write_content_file(url, login, password, delete)
            return redirect('write')

        # список сервисов
        services = enum_services_get(url, login, password)
        # список протоколов
        protocols = enum_protocols_get(url, login, password)
        # получить список файлов
        writeContent = get_write_content(url, login, password)
        if writeContent is not None:
            writeContent = sorted(writeContent, key=lambda k: k['time'], reverse=True)

        # заполнить данные
        context = {'dev': dev,
                   'writeIn': writeIn,
                   'writeOut': writeOut,
                   'services': services,
                   'protocols': protocols,
                   'writeContent': writeContent}

        # Вернуть данные
        ajax = request.GET.get("ajax")
        if ajax is not None:
            data = {'rendered_table': render_to_string('write/write.html', context=context)}
            return JsonResponse(data)

        # Вернуть сформированную страницу
        return render(request, 'write/write.html', context=context)
    except Exception as ex:
        return exception(request, ex)

def  write_download(request, name):
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

        # скачать файл
        file = get_write_content_file(url, login, password, name)
        # base64
        buffer = base64.b64decode(file)
        # Вернуть файл
        return FileResponse(BytesIO(buffer), as_attachment=True, filename=name)

    except Exception as ex:
        return exception(request, ex)
