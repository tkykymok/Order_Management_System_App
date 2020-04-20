from django import template
 
register = template.Library()
 
@register.filter(name="multiply")
def multipliy(value, args):
    return int(value * args)