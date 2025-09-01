from django import template

register = template.Library()

@register.filter
def get_item(dictionary, key):
    """
    Template filter to get item from dictionary by key.
    Usage: {{ dictionary|get_item:key }}
    """
    if hasattr(dictionary, 'get'):
        return dictionary.get(key, [])
    return []
