from django import template
from django.utils import simplejson

from ..xmlpp import get_pprint

register = template.Library()


@register.filter
def prettyprint(text):
    try:
        data = simplejson.loads(text)
        return simplejson.dumps(data, indent=4)
    except ValueError:
        pass
    if text.startswith('<?xml'):
        return get_pprint(text)

    return text

