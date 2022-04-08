from distutils.errors import LibError
from wsgiref.util import request_uri
from django.shortcuts import render
from .models import Recipe, Profile
from django.views import generic
from django.http import HttpResponsePermanentRedirect, HttpResponseRedirect
from django.urls import reverse
# Create your views here.

def IndexView(requests):
    return render(requests, 'recipes/index.html', {})

class UserView(generic.DetailView):
    model = Profile
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

def newRecipe(request, pkUser):
    try:
        title = request.POST['title']
        
        ingredientsList = ""
        ingredientsQuantities = request.POST.getlist('ingredientQuant')
        ingredientsUnits = request.POST.getlist('ingredientUnit')
        ingredientsNames = request.POST.getlist('ingredientName')
        for i in range(0, len(ingredientsQuantities)):
            quantEmpty = len(ingredientsQuantities[i]) == 0 or ingredientsQuantities[i].isspace()
            unitEmpty = len(ingredientsUnits[i]) == 0 or ingredientsUnits[i].isspace()
            nameEmpty = len(ingredientsNames[i]) == 0 or ingredientsNames[i].isspace()
            if not (quantEmpty and unitEmpty and nameEmpty):
                ingredientsList += ingredientsQuantities[i].replace(" ", "*") + " " + ingredientsUnits[i].replace(" ", "*") + " " + ingredientsNames[i].replace(" ", "*") + ","
        ingredientsList = ingredientsList[:-1] # remove last comma

        directionsList = ""
        directions = request.POST.getlist('direction')
        for d in directions:
            empty = len(d) == 0 or d.isspace()
            if not empty:
                directionsList += d + ","
        directionsList = directionsList[:-1] # remove last comma

        dietaryRestrictions = request.POST['dietaryRestrictions']
        time = request.POST['time']
        servingSize = request.POST['servingSize']
        blurb = request.POST['blurb']
        difficultyRating = request.POST['difficultyRating']

        createdBy = Profile.objects.get(pk=pkUser)
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
                            difficultyRating = difficultyRating,
                            createdBy = createdBy)
            recipe.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('recipes:recipeGallery'))

def favoriteRecipe(request, pkRecipe, pkUser):
    currentRecipe = Recipe.objects.get(pk=pkRecipe)
    currentUser = Profile.objects.get(pk=pkUser)
    currentRecipe.favoritedBy.add(currentUser)
    currentRecipe.save()

    return HttpResponsePermanentRedirect('/recipes/' + str(pkRecipe)) # redirect back to current recipe
    # https://stackoverflow.com/questions/51464131/multiple-parameters-url-pattern-django-2-0

def followUser(request, pkFollow, pkUser):
    userToFollow = Profile.objects.get(pk=pkFollow)
    currentUser = Profile.objects.get(pk=pkUser)
    currentUser.following.add(userToFollow)
    currentUser.save()
    return HttpResponsePermanentRedirect('/user/' + str(pkFollow)) # redirect back

def updateUserName(request, pkUser):
    currentUser = Profile.objects.get(pk=pkUser)
    currentUser.name = request.POST['name']
    currentUser.save()
    return HttpResponsePermanentRedirect('/user/' + str(pkUser)) # redirect back

def updateUserCookExp(request, pkUser):
    currentUser = Profile.objects.get(pk=pkUser)
    currentUser.cooking_experience = request.POST['cook_exp']
    currentUser.save()
    return HttpResponsePermanentRedirect('/user/' + str(pkUser)) # redirect back

def updateUserProfileImg(request, pkUser):
    currentUser = Profile.objects.get(pk=pkUser)
    # img_upload = request.FILES.get('profile_img', False)
    img_upload = request.FILES['profile_img']
    if(img_upload):
        currentUser.profile_img = img_upload
        currentUser.save()
    return HttpResponsePermanentRedirect('/user/' + str(pkUser)) # redirect back