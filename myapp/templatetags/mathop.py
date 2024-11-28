from django import template
from myapp import models

register = template.Library()

@register.filter(name='multiply')
def multiply(price, weight ):
    return price * weight


