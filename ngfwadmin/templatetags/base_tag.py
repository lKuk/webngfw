from django import template
register = template.Library()


@register.simple_tag()
def is_active(request, urllist, text):
    list = urllist.split()
    name = request.resolver_match.url_name
    if name in list:
        return text
    return ''
