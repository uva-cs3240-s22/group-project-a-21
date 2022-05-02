from django import template
from recipes.models import Profile, Recipe

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
    # if float(number) == 2.5: # python rounds 2.5 to 2; for our purposes, we want 3
    #     return 3
    return float(number)//1

@register.filter(name='parseIntFiveMinus') 
def parseInt(number):
    # if float(number) == 2.5: # python rounds 2.5 to 2; for our purposes, we want 3
    #     return 3
    return 5 - float(number)//1

@register.simple_tag
def follow(follower, followed):
    return Profile.objects.get(pk=followed) in Profile.objects.get(pk=follower).following.all()

@register.simple_tag
def favorite(profile, recipe):
    return Recipe.objects.get(pk=recipe) in Profile.objects.get(pk=profile).favorites.all()

@register.simple_tag
def allDeleted(profilePK, category):
    profile = Profile.objects.get(pk=profilePK)
    if category == "create" and profile.create.all():
        return profile.create.all()[0].title == "[deleted]" and len(profile.create.all()) == 1
        # return "aaa"
        #     return True
        # else:
        #     return False
        # if len(profile.create.all().filter(title="[deleted]")) == len(profile.create.all()):
        #     if len(profile.create.all()) > 0:
        #         return True
    if category == "favorite":
        return len(profile.favorites.all().filter(title="[deleted]")) == len(profile.favorites.all()) and len(profile.favorites.all()) > 0
    