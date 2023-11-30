from ngfwadmin.views.connect.connect import dev
from ngfwadmin.views.debug.debug import *
from ngfwadmin.rest.rules.history import *

from django.shortcuts import redirect, render


# Страница истории изменений правил
def history(request):
    try:
        # проверка подключения
        if 'url' not in dev:
            return redirect('connect')

        # восстановить
        date = request.GET.get("date")
        if date is not None:
            history_set(dev['url'], date)
            return redirect('rules')

        # получить таблицу истории
        result = history_get(dev['url'])

        # преобразовать в словарь
        history = []
        for i in range(len(result['date'])):
            row = {'id': i, 'date': result['date'][i]}
            history.append(row)

        # сортировка по доте
        sorted_history = sorted(history, key=lambda k: k['date'], reverse=True)

        # отобразить страницу с историей
        context = {'dev': dev,
                   'history': sorted_history}
        return render(request, 'rules/history/history.html', context=context)

    # обработка ошибок
    except Exception as ex:
        return exception(request, ex)
