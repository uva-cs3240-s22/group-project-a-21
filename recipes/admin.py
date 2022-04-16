from django.contrib import admin
from .models import Recipe, Profile, Review
# Register your models here.

admin.site.register(Recipe)
admin.site.register(Profile)
admin.site.register(Review)
