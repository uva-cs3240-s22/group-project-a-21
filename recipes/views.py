# /***************************************************************************************
# *  REFERENCES
# *  Title: Django Google Authentication using django-allauth
# *  Author: Muhd Rahiman
# *  Date: Feb 27, 2021 (Last Updated on Oct 28, 2021)
# *  URL: https://dev.to/mdrhmn/django-google-authentication-using-django-allauth-18f8
# 
# *  Title: multiple parameters url pattern django 2.0
# *  Author: user9723456, philmaweb
# *  Publication Date: 7/22/2018
# *  URL: https://stackoverflow.com/questions/51464131/multiple-parameters-url-pattern-django-2-0


# *  Title: Django Filter And Pagination Example
# *  Author: Zhao Song
# *  Publication Date: N/A 
# *  URL: https://www.dev2qa.com/django-filter-and-pagination-example/ 

# *  Title: Override get() in Django Class Based View to Filter
# *  Author: Berislav Lopac
# *  Publication Date: May 28, 2014
# *  URL: https://stackoverflow.com/questions/15552267/override-get-in-django-class-based-view-to-filter

# *  Title: Class-based Views
# *  Author: Chad G Hansen, Greg Reeve
# *  Publication Date: May 28, 2014
# *  URL: https://django-advanced-training.readthedocs.io/en/latest/features/class-based-views/ 

# *  Title: Django class based post-only view
# *  Author: Andreas Schosser
# *  Publication Date: Apr 26, 2016
# *  URL: https://stackoverflow.com/questions/36859618/django-class-based-post-only-view 

# ***************************************************************************************/

from distutils.errors import LibError
from re import template
import re
import io
from wsgiref.util import request_uri
from django.shortcuts import get_object_or_404, render
from .models import Recipe, Profile, RecipeImage, Review
from django.views import generic
from django.http import HttpResponsePermanentRedirect, HttpResponseRedirect, FileResponse 
from django.urls import reverse
from django.contrib.auth import logout
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import letter
from django.templatetags.static import static
import textwrap
# Create your views here.

# def IndexView(requests):
#     return render(requests, 'recipes/index.html', {})
class IndexView(generic.ListView):
    template_name='recipes/index.html'
    context_object_name = 'latest_recipe_list'
    def get_queryset(self):
        return Recipe.objects.all().order_by("-id")

class UserView(generic.DetailView):
    model = Profile
    template_name = 'recipes/user.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # print(context)
        context['tab'] = self.kwargs['tab'] if ('tab' in self.kwargs) else 'basic'
        # if 'tab' in self.kwargs:
        #     context['tab'] = self.kwargs['tab']
        # else:
        #     context['tab'] = 'basic'
        return context

def userLogout(request):
    logout(request)
    return HttpResponsePermanentRedirect('/')

# def userTab(request, pk, tab):
#     context = {'tab': tab}
#     return render(request, 'recipes/user.html', context)

class RecipeGalleryView(generic.ListView):
    template_name = 'recipes/recipeGallery.html'
    context_object_name = 'latest_recipe_list'

    def get_queryset(self):
        return Recipe.objects.all()
    
    def post(self, request):
        if (len(self.request.POST)) == 0:    
            self.object_list = Recipe.objects.all()
            context = self.get_context_data(object_list=self.object_list)
            return self.render_to_response(context)
        else:
            time = request.POST['time']
            servingSize = request.POST['servingSize']
            difficultyRating = request.POST['difficultyRating']

            recipes = Recipe.objects.all()
            if time != "":
                recipes = recipes.filter(time__lte=time)
            if servingSize != "":
                recipes = recipes.filter(servingSize__gte=servingSize)
            if difficultyRating !="":
                recipes = recipes.filter(difficultyRating__lte=difficultyRating)
            self.object_list = recipes
            context = self.get_context_data(object_list=self.object_list)
            print(recipes)
            return self.render_to_response(context)


class RecipeView(generic.DetailView):
    model = Recipe
    template_name = 'recipes/recipe.html'
    # return render(requests, 'recipes/recipe.html', {})
    def post(self, request, *args, **kwargs):
        rating = request.POST.get('rating', 3)
        rating = rating[0]
        review_text = request.POST.get('content', '')
        recipe = self.get_object()
        user = self.request.user

        pkRecipe = self.kwargs.get('pk')
        review = Review.objects.create(recipe=recipe, rating=rating, review_text=review_text, user=user)

        # returns to recipe gallery
        # would be useful to redirect to a page which allows the user to share the recipe, since they used it
        return HttpResponsePermanentRedirect('/recipes/' + str(pkRecipe))

class EnterRecipeView(generic.ListView):
    model = Recipe
    template_name = 'recipes/enterRecipe.html'

def newRecipe(request, pkUser, fork, pkRecipe):
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
                directionsList += d + "`"
        directionsList = directionsList[:-1] # remove last comma

        dietaryRestrictions = request.POST['dietaryRestrictions']
        time = request.POST['time']
        servingSize = request.POST['servingSize']
        blurb = request.POST['blurb']
        difficultyRating = request.POST['difficultyRating']

        recipe_img = request.FILES.getlist('recipe_img', False)

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
            if(recipe_img):
                for img in recipe_img:
                    if(img):
                        recipeImage = RecipeImage(image=img, recipe=recipe)
                        recipeImage.save()
            if fork: # if applicable, add this new recipe to old recipe's list of inspiredForks
                recipe.forkedBy = Recipe.objects.get(pk=pkRecipe)
                recipe.save()
                # oldRecipe = Recipe.objects.get(pk=pkRecipe)
                # oldRecipe.inspiredForks.add(recipe)
                # oldRecipe.save()

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
    # Citation for <multiple parameters url pattern django 2.0> at top of file

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
    img_upload = request.FILES.get('profile_img', False)
    # img_upload = request.FILES['profile_img']
    if(img_upload):
        currentUser.profile_img = img_upload
        currentUser.save()
    return HttpResponsePermanentRedirect('/user/' + str(pkUser)) # redirect back

def forkRecipe(request, pk):
    # Render new recipe into html
    obj = get_object_or_404(Recipe, id=pk)
    # newRecipe = Recipe.objects.create(title = obj.title)
    # context = {'newrecipe': newRecipe}
    context = {'oldrecipe': obj}
    return render(request, 'recipes/forkRecipe.html', context)

# Generate PDF file of recipe
def recipe_pdf(request, pk):
    # create buffer and canvas
    buf = io.BytesIO()
    canv = canvas.Canvas(buf, pagesize=letter, bottomup=0)
    
    # text object
    text_ob = canv.beginText()
    text_ob.setTextOrigin(inch, inch)
    recipe = get_object_or_404(Recipe, id=pk)
    # add text
    canv.setFont("Helvetica-Bold", 28)
    canv.drawCentredString(4.25*inch, 75, recipe.title)
    
    subtitle = str("Time Required: " + str(recipe.time) + " minutes | Serving Size: " + 
                   str(recipe.servingSize) + " | Dietary Restrictions: " + recipe.dietaryRestrictions + " | Difficulty: " + str(recipe.difficultyRating) + "/10" )
    
    canv.setFont("Times-Italic", 12)
    canv.drawCentredString(4.25*inch, 100, subtitle)
    canv.setFont("Helvetica-Bold", 20)
    canv.drawCentredString(4.25*inch, 135, "Ingredients List")
    
    ingredients = recipe.ingredientsList.replace("*", " ")
    l = ingredients.split(",")

    canv.setFont("Times-Roman", 12)
    
    space = 0
    for i in range(0, len(l), 2):
        space = i*10
        if (i == len(l) - 1):
            canv.drawCentredString(4.25*inch, 158 + 10*i, l[i])
        else:
            canv.drawCentredString(5.5*inch, 158 + 10*i, l[i])
            canv.drawCentredString(3.0*inch, 158 + 10*i, l[i+1])           
        
    directions = recipe.directionsList.replace("*", " ")
    l2 = directions.split("`")
   
    canv.setFont("Helvetica-Bold", 20)
    canv.drawCentredString(4.25*inch,  158 + 30 + space, "Directions")

    canv.setFont("Times-Roman", 12)
    directionStart = 158 + 30 + space + 23 # distance between Direction text and actual directions
    rows = 0
    for i in range(len(l2)):
        print(l2[i])
        limit = 95
        
        if len(l2[i]) > limit:
            wraps = textwrap.wrap(l2[i], limit)
            canv.drawString(1*inch, directionStart + 15*(rows+i), str(i+1) + ". " + wraps[0])
            for j in range(1, len(wraps)):
                print("here")
                canv.drawString(1*inch, directionStart + 15*(i+rows+j), "    " + wraps[j])
                rows += 1
        else:
            canv.drawString(1*inch, directionStart + 15*(rows+i), str(i+1) + ". " + l2[i])

      
    # Footer
    canv.drawInlineImage("recipes/static/recipes/wom_logo.png", 3.8*inch, 8.45*inch, 1*inch, 1*inch)
    canv.setFont("Times-Italic", 12)
    canv.drawCentredString(4.25*inch, 10.5*inch, "Thank you for using Word of Mouth!") 
    canv.setFont("Times-Italic", 10) 
    canv.drawCentredString(4.25*inch, 10.75*inch, "Thumay Huynh, Alex Pfoser, Rishi Mukherjee, Alex Taing, Lilian Zhang")  
    canv.showPage()
    canv.save()
    
    buf.seek(0)
    file_name = str(recipe.title + "WOM.pdf")
    file_name = file_name.replace(" ", "_")
    return FileResponse(buf, as_attachment=True, filename=file_name)
    