from django.shortcuts import render


# Страница исключений
def exception(request, ex):
    context = {'ex': ex,
               'name': 'Exception'}
    return render(request, 'Debug/error.html', context=context)


# Страница ошибки
def error(request):
    return render(request, 'Debug/error.html', context={'name': 'Error: 404 страница не найдена'})
