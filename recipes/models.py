from msilib.schema import Directory
from django.db import models
from django.contrib import admin

# Create your models here.

'''
Note for future development:
    Separate models for Ingredients and Directions lists
    (i.e. a model linking ingredients to recipes, so that ingredients )
'''
class Recipe(models.Model):
    title = models.CharField(max_length=200)
    # post_date = models.DateTimeField('date published')
    ingredientsList = models.CharField(max_length=1000)
    directionsList = models.CharField(max_length=5000)
    dietaryRestrictions = models.CharField(max_length=200)
    time = models.IntegerField(default=0)
    servingSize = models.IntegerField(default=1)

    def __str__(self):
        return self.title



