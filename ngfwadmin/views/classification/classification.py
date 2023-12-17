from django.shortcuts import redirect, render

from ngfwadmin.views.connect.dev import dev_get
from ngfwadmin.views.debug.error import exception


# Страница протокола arp
def classification(request):
    try:
        # Подключение
        dev = dev_get(request)
        # Проверка подключения
        if 'url' not in dev:
            return redirect('connect')
        # подключение
        url = dev.get('url')

        # Данные страницы
        context = {'dev': dev}
        # Вернуть сформированную страницу
        return render(request, 'classification/classification.html', context=context)
    except Exception as ex:
        return exception(request, ex)
