import math

from django import template

register = template.Library()


@register.simple_tag()
def is_active(request, urllist, text):
    list = urllist.split()
    name = request.resolver_match.url_name
    if name in list:
        return text
    return ''


@register.simple_tag()
def count_sub(rule):
    l = len(rule['sub'])
    value = 'Подправил: ' + str(l) + 'шт.'
    return value


@register.simple_tag()
def replace(value, strOld, strNew):
    strOld = strOld.replace('\\t', '\t')
    strOld = strOld.replace('\\n', '\n')
    strOld = strOld.replace('\\n', '\n')
    strNew = strNew.replace('\\t', '\t')
    strNew = strNew.replace('\\n', '\n')
    strNew = strNew.replace('\\n', '\n')
    value = value.replace(strOld, strNew)
    return value



@register.simple_tag()
def value_in_content(value, content):
    value = '[' + value + ']'
    content = content.replace('\r', '')
    content = content.replace('\n', '][')
    content = '[' + content + ']'
    if(value in content):
        return 'selected'
    return ''


@register.simple_tag()
def si_format(size):
    if size == 0:
        return size
    pwr = math.floor(math.log(size, 1024))
    suff = ["", "К", "М", "Г", "Т", "П"]
    if size > 1024 ** (len(suff) - 1):
        return "не знаю как назвать такое число :)"
    return f"{size / 1024 ** pwr:.1f} {suff[pwr]}"


@register.simple_tag()
def permissions_text(permissions, login, value, text):
    if permissions.get(login) == value:
        return text
    return ''



@register.simple_tag()
def check_permissions(dev, paths, method, text):
    if isinstance(dev, dict) == False:
        return text
    if 'permissions' not in dev:
        return text
    permissions = dev.get('permissions')
    if isinstance(permissions, list) == False:
        return text
    paths = paths.split("||")

    # все проверяемые привилегии
    for path in paths:
        method = method.lower().strip()
        path = path.strip('/').strip().lower()
        # все доступные привилегии
        for p in permissions:
            m = p.get('method').lower()
            p = p.get('path').strip('/').strip().lower()
            # путь совпал
            if path == p:
                # проверяем доступ
                if m == 'readwrite':
                    return ''
                if m == 'readonly' and method == 'readonly':
                    return ''
    return text
