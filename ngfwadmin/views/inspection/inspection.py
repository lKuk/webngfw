from django.http import HttpResponse
from django.shortcuts import redirect, render

from ngfwadmin.views.debug.error import exception
from ngfwadmin.views.connect.connect import get_connect
from ngfwadmin.rest.inspection.inspection import ca_get, status_set, ca_set, status_get


# Страница состояния портов
def inspection(request):
    try:
        # Подключение
        dev = get_connect()
        # Проверка подключения
        if 'url' not in dev:
            return redirect('connect')
        # подключение
        url = dev.get('url')

        # Определить ключ и сертификат
        ca = ca_get(url)
        key = ca['key']
        cer = ca['cer']

        # изменить статус
        checked = request.GET.get("checked")
        if checked is not None:
            status_set(url, checked)
            return

        # Скачать ключ
        get_key = request.GET.get("get_key")
        if get_key is not None:
            return HttpResponse(key)

        # Скачать сертификат
        get_cer = request.GET.get("get_cer")
        if get_cer is not None:
            return HttpResponse(cer)

        labelKey = 'Выберете файл ключа для загрузки'
        labelCer = 'Выберете файл сертификата загрузки'
        # Загрузка файлов
        if request.method == 'POST':
            # Загрузить правила
            if 'key' in request.FILES:
                file = request.FILES['key']
                content = ''
                for chunk in file.chunks():
                    content += chunk.decode("utf-8")
                ca_set(url, content, cer)
                labelKey = 'Загрузка ключа выполнена успешно!'
            # Загрузить конфигурацию
            if 'cer' in request.FILES:
                file = request.FILES['cer']
                content = ''
                for chunk in file.chunks():
                    content += chunk.decode("utf-8")
                ca_set(url, key, content)
                labelCer = 'Загрузка сертификата выполнена успешно!'

        ca = ca_get(url)
        status = status_get(url)
        context = {'ca': ca,
                   'dev': dev,
                   'status': status,
                   'labelKey': labelKey,
                   'labelCer': labelCer}
        # Вернуть сформированную страницу
        return render(request, 'inspection/inspection.html', context=context)
    except Exception as ex:
        return exception(request, ex)
