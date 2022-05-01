from django import template
from recipes.models import Profile

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

@register.filter(name='times') 
def times(number):
    return range(number)

@register.simple_tag
def index(**kwargs):
    value = kwargs['value']
    number = kwargs['number']
    return value.split(" ")[number]

@register.simple_tag
def indexName(**kwargs):
    value = kwargs['value']
    number = kwargs['number']
    return value.split(" ")[number].replace("*", " ")

@register.filter(name='parseInt') 
def parseInt(number):
    if float(number) == 2.5: # python rounds 2.5 to 2; for our purposes, we want 3
        return 3
    return round(float(number))

@register.filter(name='parseIntFiveMinus') 
def parseInt(number):
    if float(number) == 2.5: # python rounds 2.5 to 2; for our purposes, we want 3
        return 3
    return 5 - round(float(number))

@register.filter(name='follows')
def follows(pks):
    return Profile.objects.get(pk=int(pks.split(",")[1])) in Profile.objects.get(pk=int(pks.split(",")[0])).following.all()

@register.simple_tag
def follow(follower, followed):
    return Profile.objects.get(pk=followed) in Profile.objects.get(pk=follower).following.all()