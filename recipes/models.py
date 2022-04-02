# from msilib.schema import Directory
from email.policy import default
from django.db import models
from django.contrib import admin
from django.core.validators import MaxValueValidator, MinValueValidator

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
    servingSize = models.PositiveSmallIntegerField(default=1)
    blurb = models.CharField(max_length=1000, default="no blurb entered")
    difficultyRating = models.PositiveSmallIntegerField(
        default=3,
        validators=[
            MaxValueValidator(10),
            MinValueValidator(1)
        ]
        # https://stackoverflow.com/questions/849142/how-to-limit-the-maximum-value-of-a-numeric-field-in-a-django-model
    )

    def __str__(self):
        return self.title
    

''' 
Recipe Review
Links back to specific recipe
If Recipe is deleted, all related Reviews are deleted as well
'''
class Review(models.Model):
    recipe = models.ForeignKey(Recipe, related_name='reviews', on_delete=models.CASCADE);
    
    review_text = models.TextField(blank=True, null=True)
    rating = models.IntegerField()
    
    


