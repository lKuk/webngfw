from ngfwadmin.rest.ipsids.ipsids import *
from ngfwadmin.views.connect.connect import *

from django.http import HttpResponse
from django.shortcuts import redirect, render


# Страница состояния портов
def ipsids(request):
    try:
        # Подключение
        dev = get_connect()
        # Проверка подключения
        if 'url' not in dev:
            return redirect('connect')
        # Подключение
        url = dev.get('url')

        # Изменить статус
        checked = request.GET.get("checked")
        if checked is not None:
            status_set(url, checked)
            return

        # Скачать правила
        get_rules = request.GET.get("get_rules")
        if get_rules is not None:
            rules = rules_get(url)
            return HttpResponse(rules)

        # Скачать конфигурацию
        get_config = request.GET.get("get_config")
        if get_config is not None:
            config = configuration_get(url)
            return HttpResponse(config)

        labelRule = 'Выберете файл загрузки правил'
        labelConfig = 'Выберете файл загрузки конфигурации'
        # Загрузка файлов
        if request.method == 'POST':
            # Загрузить правила
            if 'rules' in request.FILES:
                file = request.FILES['rules']
                content = ''
                for chunk in file.chunks():
                    content += chunk.decode("utf-8")
                rules_set(url, content)
                labelRule = 'Загрузка правил выполнена успешно!'
            # Загрузить конфигурацию
            if 'config' in request.FILES:
                file = request.FILES['config']
                content = ''
                for chunk in file.chunks():
                    content += chunk.decode("utf-8")
                configuration_set(url, content)
                labelConfig = 'Загрузка конфигурации выполнена успешно!'

        # Данные страницы
        status = status_get(url)
        context = {'dev': dev,
                   'status': status,
                   'labelRule': labelRule,
                   'labelConfig': labelConfig}
        # Вернуть сформированную страницу
        return render(request, 'ipsids/ipsids.html', context=context)
    except Exception as ex:
        return exception(request, ex)
