from django.http import HttpResponse

from ngfwadmin.views.connect.connect import *
from ngfwadmin.rest.inspection.inspection import *

from django.shortcuts import redirect, render


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

        # изменить статус
        checked = request.GET.get("checked")
        if checked is not None:
            status_set(url, checked)
            return

        # скачать правила
        getKey = request.GET.get("getKey")
        if getKey is not None:
            Ca = ca_get(url)
            key = Ca['key']
            return HttpResponse(key)

            # скачать правила
        getCer = request.GET.get("getCer")
        if getCer is not None:
            Ca = ca_get(url)
            cert = Ca['cer']
            return HttpResponse(cert)

        ca = ca_get(url)
        status = status_get(url)
        context = {'ca': ca,
                   'dev': dev,
                   'status': status}
        # Вернуть сформированную страницу
        return render(request, 'inspection/inspection.html', context=context)
    except Exception as ex:
        return exception(request, ex)
