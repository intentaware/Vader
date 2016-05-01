from django import template
from django.conf import settings

register = template.Library()

@register.simple_tag(takes_context=True)
def ng_app(context):
    return context.get('ng_app', False)
