from django.http import JsonResponse, HttpResponse
from django.shortcuts import redirect, render

from ngfwadmin.views.connect.dev import dev_get
from ngfwadmin.views.debug.error import exception
from ngfwadmin.rest.write.write import get_write_content, save_file
from ngfwadmin.rest.write.write import get_write_in, get_write_out, set_write_in, set_write_out


def write(request):
    try:
        # Подключение
        dev = dev_get(request)
        # Проверка подключения
        if 'url' not in dev:
            return redirect('connect')

        # подключение
        url = dev.get('url')

        writeIn = get_write_in(url)
        writeOut = get_write_out(url)
        content = get_write_content(url)

        # изменить статус
        checked = request.GET.get("write_status")
        port = request.GET.get("port")
        write = request.GET.get("write")
        if checked is not None and write is not None:
            if checked == 'true':
                status = "write"
            else:
                status = "stop"

            if write == 'writeIn':
                set_write_in(url, writeIn['write_portin'], status)
            if write == 'writeOut':
                set_write_out(url, writeOut['write_portout'], status)
            return
        # Изменить порт
        if port is not None and write is not None:
            if write == 'writeInSave':
                if writeIn['write_statusin'] == 'pass':
                    writeIn['write_statusin'] = 'stop'
                set_write_in(url, port, writeIn['write_statusin'])
            if write == 'writeOutSave':
                if writeOut['write_statusout'] == 'pass':
                    writeOut['write_statusout'] = 'stop'
                set_write_out(url, port, writeOut['write_statusout'])
            return

        pcap = request.GET.get('pcap')
        if pcap is not None:
            file = save_file(url, pcap)
            return HttpResponse(file)

        context = {'dev': dev,
                   'writeIn': writeIn,
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
