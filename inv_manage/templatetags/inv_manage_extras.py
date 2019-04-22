from django import template
register = template.Library()

@register.filter(is_safe=True)
def add(value):
    return value+1

@register.filter(is_safe=True)
def subtract(value):
    return value-1

