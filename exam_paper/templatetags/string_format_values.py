from django import template

register = template.Library()

@register.simple_tag
def format_values(format, *args):
    return format % args