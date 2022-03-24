from django.shortcuts import render
from .models import Recipe
from django.views import generic
# Create your views here.

# both of these should be classes? or at least UserView should be a DetailView maybe
def IndexView(requests):
    return render(requests, 'recipes/index.html', {})

def UserView(requests):
    return render(requests, 'recipes/user.html', {})

def RecipeGalleryView(requests):
     return render(requests, 'recipes/recipeGallery.html', {})

class RecipeView(generic.DetailView):
    model = Recipe
    template_name = 'recipes/recipe.html'

    # return render(requests, 'recipes/recipe.html', {})