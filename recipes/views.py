from django.shortcuts import render
# Create your views here.

# both of these should be classes? or at least UserView should be a DetailView maybe
def IndexView(requests):
    return render(requests, 'recipes/index.html', {})

def UserView(requests):
    return render(requests, 'recipes/user.html', {})

def RecipeGalleryView(requests):
     return render(requests, 'recipes/recipeGallery.html', {})

def RecipeView(requests):
     return render(requests, 'recipes/recipe.html', {})