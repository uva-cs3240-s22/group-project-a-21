# from msilib.schema import Directory
from distutils.command.upload import upload
from email.policy import default
import profile
from django.db import models
from django.contrib import admin
from django.core.validators import MaxValueValidator, MinValueValidator
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save
from gdstorage.storage import GoogleDriveStorage

gd_storage = GoogleDriveStorage()

# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=50, blank=True)
    email = models.EmailField(max_length=50, blank=True)
    cooking_experience = models.IntegerField(default=0)
    following = models.ManyToManyField("self", blank=True, symmetrical=False)
    # profile_img = models.ImageField(upload_to="profile_img/", storage=gd_storage, default="{% static 'recipes/default_chef.png' %}")
    profile_img = models.ImageField(upload_to="profile_img/", storage=gd_storage)

    def __str__(self):
        return str(self.user)


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance, name=instance.username, email=instance.email)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
    
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
    favoritedBy = models.ManyToManyField(Profile, related_name="favorites") # a User has many favorite Recipes; a Recipe is favorited by many Users
    createdBy = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="create", default=1)
    # https://stackoverflow.com/questions/13918968/multiple-many-to-many-relations-to-the-same-model-in-django

    def get_avg_rating(self):
        reviews = Review.objects.filter(recipe=self)
        count = len(reviews)
        sum = 0
        if count != 0:
            for rvw in reviews:
                sum += rvw.rating
            return (sum/count)
        else:
            return 404

    def __str__(self):
        return self.title

class RecipeImage(models.Model):
    image = models.ImageField(upload_to="recipe_img/", storage=gd_storage, default="")
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name="images", default=1)

    def __str__(self):
        return self.image

''' 
Recipe Review
Links back to specific recipe
If Recipe is deleted, all related Reviews are deleted as well
'''
class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    recipe = models.ForeignKey(Recipe, related_name='reviews', on_delete=models.CASCADE);
    review_text = models.TextField(blank=True, null=True)
    rating = models.IntegerField()