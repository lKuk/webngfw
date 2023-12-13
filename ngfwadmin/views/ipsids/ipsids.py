from django.http import HttpResponse
from django.shortcuts import redirect, render

from ngfwadmin.views.connect.dev import dev_get
from ngfwadmin.views.debug.error import exception
from ngfwadmin.rest.inspection.inspection import status_set
from ngfwadmin.rest.ipsids.ipsids import rules_get, configuration_get, rules_set, configuration_set, status_get


# Страница состояния портов
def ipsids(request):
    try:
        # Подключение
        dev = dev_get(request)
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
