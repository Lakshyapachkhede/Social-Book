from django import template

register = template.Library()

@register.filter(name='instanceof')
def isinstanceof(value, class_name):
    return value.__class__.__name__.lower() == class_name.lower()