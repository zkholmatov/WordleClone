from django import template

register = template.Library()

@register.filter
def index(sequence, i):
    try:
        return sequence[i]
    except (IndexError, KeyError, TypeError):
        return ''
    
@register.filter
def zerotoone(index):
    try:
        return index+1
    except (IndexError, KeyError, TypeError):
        return 0