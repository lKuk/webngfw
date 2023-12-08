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
        # подключение
        url = dev.get('url')

        # изменить статус
        checked = request.GET.get("checked")
        if checked is not None:
            status_set(url, checked)
            return

        # сохранить ipsids
        if request.method == 'POST':
            # добавить список
            if 'btnIpsIdsUpdate' in request.POST:
                # Получить параметры
                rules = request.POST.get('rules')
                config = request.POST.get('config')
                # сохранить параметры
                rules_set(url, rules)
                configuration_set(url, config)

        # Данные страницы
        status = status_get(url)
        rules = 'rules test 11111' #rules_get(url)
        config = 'config test 22222' #configuration_get(url)
        context = {'dev': dev,
                   'rules': rules,
                   'config': config,
                   'status': status}
        # Вернуть сформированную страницу
        return render(request, 'ipsids/ipsids.html', context=context)
    except Exception as ex:
        return exception(request, ex)
