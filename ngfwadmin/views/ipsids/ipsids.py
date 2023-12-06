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

        # # Вернуть данные
        # rules = request.GET.get("rules")
        # if rules is not None:
        #     #context = rules_get(url)
        #     return HttpResponse('123') #(context)
        #
        # # Вернуть данные
        # config = request.GET.get("config")
        # if config is not None:
        #     context = configuration_get(url)
        #     return HttpResponse(context)

        rules = rules_get(url)
        status = status_get(url)
        config = configuration_get(url)
        context = {'dev': dev,
                   'rules': rules,
                   'config': config,
                   'status': status}
        # Вернуть сформированную страницу
        return render(request, 'ipsids/ipsids.html', context=context)
    except Exception as ex:
        return exception(request, ex)
