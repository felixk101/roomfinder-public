from django import template
from django.contrib.staticfiles import finders
from django.utils.html import escape

register = template.Library()


@register.simple_tag
def includestatic(path, encoding='UTF-8'):
    file_path = finders.find(path)
    with open(file_path, "r", encoding=encoding) as f:
        string = f.read()
        return escape(string)