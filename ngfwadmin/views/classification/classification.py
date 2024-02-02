from django.shortcuts import redirect, render

from ngfwadmin.views.connect.dev import dev_get
from ngfwadmin.views.debug.error import exception
from ngfwadmin.rest.classification.classification import classification_get, classification_set


# Страница протокола arp
def classification(request):
    try:
        # Подключение
        dev = dev_get(request)
        # Проверка подключения
        if 'url' not in dev or 'login' not in dev or 'password' not in dev:
            return redirect('connect')
        # подключение
        url = dev.get('url')
        login = dev.get('login')
        password = dev.get('password')

        classification = classification_get(url, login, password)
        cert_enable = classification.get('cert_enable')
        signature_enable = classification.get('signature_enable')
        service_class_enable = classification.get('service_class_enable')
        class_enable = classification.get('class_enable')

        checked = request.GET.get('checked')
        param = request.GET.get('param')
        if checked is not None:
            checked = str(checked).lower()
            if param == "cert_enable":
                classification_set(url, login, password, checked, signature_enable, service_class_enable, class_enable)
            if param == "signature_enable":
                classification_set(url, login, password, cert_enable, checked, service_class_enable, class_enable)
            if param == "service_class_enable":
                classification_set(url, login, password, cert_enable, signature_enable, checked, class_enable)
            if param == "class_enable":
                classification_set(url, login, password, cert_enable, signature_enable, service_class_enable, checked)
            return

            # Данные страницы
        context = {'dev': dev,
                   'classification': classification}
        # Вернуть сформированную страницу
        return render(request, 'classification/classification.html', context=context)
    except Exception as ex:
        return exception(request, ex)
