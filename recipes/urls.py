from django.contrib import admin
from django.urls import path, include
from . import views

app_name = "recipes"
urlpatterns = [
    # path('', views.IndexView, name='index'),
    path('', views.IndexView.as_view(), name='index'),
    # path('user/', views.UserView, name='user'),
    path('user/<int:pk>/', views.UserView.as_view(), name='user'),
    path('user/<int:pk>/<tab>/', views.UserView.as_view(), name='userTab'),
    path('user/logout/', views.userLogout, name='userLogout'),
    path('recipes/', views.RecipeGalleryView.as_view(), name='recipeGallery'),
    path('recipes/enter-recipe/', views.EnterRecipeView.as_view(), name='enterRecipe'),
    path('recipes/new-recipe/<int:pkUser>/<int:fork>/<int:pkRecipe>', views.newRecipe, name='newRecipe'),
    # <int:fork> = fork? 1:0; only read <int:pkRecipe> if fork=1
    path('recipes/<int:pk>/', views.RecipeView.as_view(), name='recipe'),
    path('recipes/fork/<int:pk>/', views.forkRecipe, name='fork'),
    path('recipes/favorite-recipe/<int:pkRecipe>/<int:pkUser>', views.favoriteRecipe, name='favoriteRecipe'),
    path('user/follow-user/<int:pkFollow>/<int:pkUser>', views.followUser, name='followUser'),
    path('user/update/name/<int:pkUser>', views.updateUserName, name='updateUserName'),
    path('user/update/cook_exp/<int:pkUser>', views.updateUserCookExp, name='updateUserCookExp'),
    path('user/update/profile_img/<int:pkUser>', views.updateUserProfileImg, name='updateUserProfileImg'),
    
    # pdf generation
    path("recipes/recipe_pdf/<int:pk>/", views.recipe_pdf, name = 'recipe_pdf'),
    
]