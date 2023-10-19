import json
import requests

from django.http import HttpResponse
from django.shortcuts import render, redirect

# Create your views here.


url = 'http://192.168.1.145:18888'

menu = [{'title': "Правила NGFW", 'url_name': 'rules'},
        {'title': "Описание", 'url_name': 'description'}]

def rules(request):
    if request.method == 'POST':
        # получили прошлый json
        jsonString = request.POST['details']
        jsonString = jsonString.replace("\'", "\"")
        details = json.loads(jsonString)
        # заполнили новыпи параметрами
        id = request.POST['id']
        if id != 0:
            details['id'] = request.POST['id']
            details['name'] = request.POST['name']
            details['rtype'] = request.POST['rtype']
            details['description'] = request.POST['description']
            # отправить rest на сохнанение правила
            resp = requests.put(f"{url}/rules/{id}", json=details)
            # проверка ошибки
            if resp.status_code != 200:
                return HttpResponse("Error")
            response = redirect('rules')
            return response
        else:
            return HttpResponse("Добавление правила еще не сделано...")

    response = requests.get(f"{url}/rules")
    details = response.json()
    context = {'menu': menu,
               'details': details,
               'title': 'Правила NGFW',}
    return render(request, 'rules/rules.html', context=context)

def rule(request, id):
    readonly = ''
    if id != 0:
        readonly = 'readonly'
    response = requests.get(f"{url}/rules/{id}")
    details = response.json()
    context = {'menu': menu,
               'details': details,
               'readonly': readonly,
               'title': 'Правило'}
    return render(request, 'rules/rule.html', context=context)

def description(request):
    context = {'title': 'Описание', 'menu': menu}
    return render(request, 'rules/description.html', context=context)






