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

        # скачать правила
        getRules = request.GET.get("getRules")
        if getRules is not None:
            rules = rules_get(url)
            return HttpResponse(rules)

        getCongig = request.GET.get("getConfig")
        if getCongig is not None:
            config = configuration_get(url)
            return HttpResponse(config)

        postRules = request.GET.get("postRules")
        # добавить список
        if postRules is not None:
            # сохранить параметры
            rules_set(url, postRules)

        # rules = rules_get(url)
        # config = configuration_get(url)

        # Данные страницы
        status = status_get(url)
        context = {'dev': dev,
                   'status': status}
        # Вернуть сформированную страницу
        return render(request, 'ipsids/ipsids.html', context=context)
    except Exception as ex:
        return exception(request, ex)
