from django import template

register = template.Library()


@register.simple_tag()
def get_navbar():
    return [
        {'title': 'ARTICLES', 'url_name': 'blog'},
        {'title': 'ABOUT', 'url_name': 'about'}
    ]