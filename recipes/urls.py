from django.contrib import admin
from django.urls import path, include
from . import views

app_name = "recipes"
urlpatterns = [
    path('', views.IndexView, name='index'),
    path('user/', views.UserView, name='user'),
    path('recipes/', views.RecipeGalleryView, name='recipeGallery'),
    # path('recipe/<int:recipe_id>/', views.RecipeView, name='recipe')
]