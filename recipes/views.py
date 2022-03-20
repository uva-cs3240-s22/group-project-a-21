from django.shortcuts import render
from django.views import generic

from .models import User

# Create your views here.

# both of these should be classes? or at least UserView should be a DetailView maybe
def IndexView(requests):
    return render(requests, 'recipes/index.html', {})

# def UserView(requests):
#     return render(requests, 'recipes/user.html', {})
class UserView(generic.DetailView):
    model = User
    template_name = 'recipes/user.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

def RecipeGalleryView(requests):
     return render(requests, 'recipes/recipeGallery.html', {})

def RecipeView(requests):
     return render(requests, 'recipes/recipe.html', {})