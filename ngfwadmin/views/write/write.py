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
        content = get_write_content(url)

        # параметры
        pcap = request.GET.get('pcap')
        port = request.GET.get("port")
        write = request.GET.get("write")
        delete = request.GET.get("delete")
        checked = request.GET.get("write_status")

        # изменить статус
        if checked is not None and write is not None:
            # значение статуса
            status = "stop"
            if checked == 'true':
                status = "write"
            # запись входящего
            if write == 'writeIn':
                set_write_in(url, writeIn['write_portin'], status)
            # запись исходящего
            if write == 'writeOut':
                set_write_out(url, writeOut['write_portout'], status)
            return

        # изменить порт
        if port is not None and write is not None:
            # сохранить порты входящего
            if write == 'writeInSave':
                if writeIn['write_statusin'] == 'pass':
                    writeIn['write_statusin'] = 'stop'
                set_write_in(url, port, writeIn['write_statusin'])
            # сохранить порты исходящего
            if write == 'writeOutSave':
                if writeOut['write_statusout'] == 'pass':
                    writeOut['write_statusout'] = 'stop'
                set_write_out(url, port, writeOut['write_statusout'])
            return

        # скачать файл
        if pcap is not None:
            file = get_write_content_file(url, pcap)
            return HttpResponse(file)

        # удалить файл
        if delete is not None:
            delete_write_content_file(url, delete)
            return redirect('write')

        # заполнить данные
        context = {'dev': dev,
                   'writeIn': writeIn,
                   'writeOut': writeOut,
                   'content': content}

        # Вернуть данные
        ajax = request.GET.get("ajax")
        if ajax is not None:
            return JsonResponse(context)

        # Вернуть сформированную страницу
        return render(request, 'write/write.html', context=context)
    except Exception as ex:
        return exception(request, ex)
