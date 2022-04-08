from django.contrib import admin
<<<<<<< HEAD
from .models import Recipe, Review, Profile
# Register your models here.
admin.site.register(Recipe)
admin.site.register(Review)

admin.site.register(Recipe)
=======
from .models import Recipe, Profile
# Register your models here.

admin.site.register(Recipe)
admin.site.register(Profile)
>>>>>>> origin/main

