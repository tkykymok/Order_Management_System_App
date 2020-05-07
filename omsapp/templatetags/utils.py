from django import template
 
register = template.Library()
 
@register.filter(name="multiply")
def multiply(value, args):
    return int(value * args)


@register.filter
def in_group(user, team_name):
    if user.groups.filter(name=team_name).exists():
        return True
    else:
        return False