from django.contrib import admin
from django.urls import path, include
from . import views

app_name = "recipes"
urlpatterns = [
    path('', views.IndexView, name='index'),
    path('user/', views.UserView, name='user'),
    path('recipes/', views.RecipeGalleryView, name='recipeGallery'),
    path('recipe/', views.RecipeView, name='recipe'), # this is the individual recipe page; should figure out how to add recipe_id as part of url later
    # path('recipe/<int:recipe_id>/', views.RecipeView, name='recipe')
]