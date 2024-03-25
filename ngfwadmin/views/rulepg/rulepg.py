import json
import math

import psycopg2
from django.http import JsonResponse
from django.shortcuts import redirect, render

from ngfwadmin.views.connect.dev import dev_get
from ngfwadmin.views.debug.error import exception


# Страница правил
def rulepg(request):
    try:
        # Подключение
        dev = dev_get(request)

        # # проверка подключения
        # if 'url' not in dev or 'login' not in dev or 'password' not in dev:
        #     return redirect('connect')
        #
        # # подключение
        # url = dev.get('url')
        # login = dev.get('login')
        # password = dev.get('password')
        # connect_pg = dev.get('connect_pg')

        connect_pg = {'dbname': 'ngfw', 'host': '192.168.1.235', 'password': '111111', 'port': '5432', 'user': 'postgres'}

        # подключиться к базе данных
        connection = psycopg2.connect(user=connect_pg["user"],
                                      host=connect_pg["host"],
                                      port=connect_pg["port"],
                                      dbname=connect_pg["dbname"],
                                      password=connect_pg["password"])
        # открыть курсор к базе данных
        cursor = connection.cursor()

        # создать список
        action = ''
        if request.method == 'POST':
            # добавить список
            if 'btnInsert' in request.POST:
                action = 'new_row'


        # выполнить функцию в базе данных
        db_func = request.GET.get("db_func")
        if db_func is not None:
            try:
                db_param = request.GET.get("db_param")
                db_param = json.loads(db_param)
                cursor.callproc(db_func, db_param)
                result = cursor.fetchall()[0][0]
                connection.commit()
                result = {db_func: result}
                return JsonResponse(result)
            except Exception as ex:
                result = {db_func: str(ex) }
                return JsonResponse(result)

        # номер страницы
        page_num = request.GET.get("page_num")
        if page_num is None:
            page_num = 1
        page_num = int(page_num)
        page_len = request.GET.get("page_len")
        if page_len is None:
            page_len = 10
        page_len = int(page_len)

        # получить количество правил
        cursor.callproc('filter.web_rules_count_json') #.callproc('filter.web_rules_count')
        rules_count = cursor.fetchall()[0][0]
        rules_count = rules_count[0]['count']

        # получить наборы
        cursor.callproc('filter.web_kit_json')
        kit = cursor.fetchall()[0][0]

        # получить категории
        cursor.callproc('filter.web_cat_json')
        cat = cursor.fetchall()[0][0]

        # # получить категории с типами
        # cursor.callproc('filter.web_cat_type_json')
        # cat_type = cursor.fetchall()[0][0]

        # получить страницу с правилами
        limit = page_len
        offset = (page_num - 1) * page_len
        cursor.callproc('filter.web_rules_json', [limit,offset,action])
        rules = cursor.fetchall()[0][0]
        connection.commit()

        # получить параметры пагинации страниц
        pagination = get_pagination(rules_count, page_len, page_num)

        # отобразить страницу правил
        context = {'dev': dev,
                   'cat': cat,
                   'kit': kit,
                   'rules': rules,
                   #'cat_type': cat_type,
                   'pagination': pagination}
        return render(request, 'rulepg/rulepg.html', context=context)

    # обработка ошибок
    except Exception as ex:
        return exception(request, ex)


# Страница правил
def get_pagination(count, len, num):
    count = math.ceil(count / len)
    # список страниц
    list = []
    if count <= 7:
        for index in range(1, count + 1):
            list.append(index)
    elif num < 3:
        list = [1, 2, 3, None, count]
    elif num == 3:
        list = [1, 2, 3, 4, None, count]
    elif 3 < num < count - 2:
        list = [1, None, num - 1, num, num + 1, None, count]
    elif num == count - 2:
        list = [1, None, count - 3, count - 2, count - 1, count]
    elif num > count - 2:
        list = [1, None, count - 2, count - 1, count]
    else:
        list = [1, 2, 3, None, count - 2, count - 1, count]
    # значения пагинации
    pagination = {}
    pagination['num'] = num
    pagination['len'] = len
    pagination['list'] = list
    return pagination
