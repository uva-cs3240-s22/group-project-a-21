from django.db import models

# Create your models here.
class User(models.Model):
    name = models.CharField(max_length=30)
    email = models.CharField(max_length=50)
    cooking_experience = models.IntegerField()
    friends = models.ManyToManyField("self")
    # made_recipes = models.ManyToManyField(Recipe)
    # favorite_recipes = models.ManyToManyField(Recipe)

    def __str__(self):
        return self.name