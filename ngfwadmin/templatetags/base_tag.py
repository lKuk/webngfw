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
