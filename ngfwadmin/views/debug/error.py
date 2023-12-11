from django.shortcuts import render


# Страница ошибки
def error(request):
    # Подключение
    context = {'name': 'Error: 404 страница не найдена'}
    return render(request, 'debug/error.html', context=context)


# Страница исключений
def exception(request, ex):
    context = {'ex': ex,
               'name': 'Exception'}
    return render(request, 'debug/error.html', context=context)

