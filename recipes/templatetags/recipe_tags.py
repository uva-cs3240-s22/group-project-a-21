from django import template

register = template.Library()
@register.filter(name='split')
def split(value, arg):
    return value.split(arg)

# @register.filter(name="splitIngredientAmount")
# def splitIngredientAmount(value):
#     return value.split(" ")

@register.filter(name='replace')
def replace(value, arg):
    return value.replace(arg.split(",")[0], arg.split(",")[1])