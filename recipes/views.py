from distutils.errors import LibError
from django.shortcuts import render

import recipes
# from numpy import diff
from .models import Recipe, User
from django.views import generic
from django.http import HttpResponsePermanentRedirect, HttpResponseRedirect
from django.urls import reverse
# Create your views here.

# both of these should be classes? or at least UserView should be a DetailView maybe
def IndexView(requests):
    return render(requests, 'recipes/index.html', {})

class UserView(generic.DetailView):
    model = User
    template_name = 'recipes/user.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

# def RecipeGalleryView(requests):
#      return render(requests, 'recipes/recipeGallery.html', {})
class RecipeGalleryView(generic.ListView):
    template_name = 'recipes/recipeGallery.html'
    context_object_name = 'latest_recipe_list'
    def get_queryset(self):
        return Recipe.objects.all()

class RecipeView(generic.DetailView):
    model = Recipe
    template_name = 'recipes/recipe.html'
    # return render(requests, 'recipes/recipe.html', {})

class EnterRecipeView(generic.ListView):
    model = Recipe
    template_name = 'recipes/enterRecipe.html'

def newRecipe(request):
    try:
        title = request.POST['title']
        ingredientsList = request.POST['ingredientsList']
        directionsList = request.POST['directionsList']
        dietaryRestrictions = request.POST['dietaryRestrictions']
        time = request.POST['time']
        servingSize = request.POST['servingSize']
        blurb = request.POST['blurb']
        difficultyRating = request.POST['difficultyRating']
        # createdBy = -----
    except (KeyError):
        # Redisplay the question voting form.
        return render(request, 'recipes/enterRecipe.html', {
            # 'error_message': "Something went wrong.",
        })
    else:
        if(title != "" and ingredientsList != ""):
            recipe = Recipe(title = title,
                            ingredientsList = ingredientsList,
                            directionsList = directionsList,
                            dietaryRestrictions = dietaryRestrictions,
                            time = time,
                            servingSize = servingSize,
                            blurb = blurb,
                            difficultyRating = difficultyRating)
            recipe.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('recipes:recipeGallery'))

def favoriteRecipe(request, pkRecipe, pkUser):
    currentRecipe = Recipe.objects.get(pk=pkRecipe)
    currentUser = User.objects.get(pk=pkUser)
    currentRecipe.favoritedBy.add(currentUser)
    currentRecipe.save()

    return HttpResponsePermanentRedirect('/recipes/' + str(pkRecipe)) # redirect back to current recipe