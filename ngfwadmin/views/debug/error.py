from django.shortcuts import render

from ngfwadmin.views.connect.dev import dev_get


# Страница ошибки
def error(request):
    # Подключение
    dev = dev_get(request)
    # Содержимое ошибки
    context = {'dev': dev,
               'name': 'Error: 404 страница не найдена'}
    return render(request, 'debug/error.html', context=context)


# Страница исключений
def exception(request, ex):
    # Подключение
    dev = dev_get(request)
    # Содержимое ошибки
    context = {'ex': ex,
               'dev': dev,
               'name': 'Exception'}
    return render(request, 'debug/error.html', context=context)

