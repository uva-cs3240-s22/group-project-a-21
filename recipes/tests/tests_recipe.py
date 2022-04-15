from django.test import TestCase
from recipes.models import Recipe, Profile;
from django.contrib.auth.models import User


class RecipeTests(TestCase):

    @classmethod
    def setUpTestData(cls):
        User.objects.create(username="test1", password="password")
        User.objects.create(username="test2", password="password")
        
        recipe1= Recipe.objects.create(
            title = "test",
            ingredientsList = "ingredient 1",
            directionsList = "This is step 1",
            dietaryRestrictions = "",
            time = 60,
            servingSize = 4,
            blurb = "this is a recipe",
            difficultyRating = 3,
            createdBy = Profile.objects.get(pk=1)
        )
        recipe1.favoritedBy.set([Profile.objects.get(pk=2), Profile.objects.get(pk=1)])

    def test_get_recipe_title(self):
        recipe = Recipe.objects.get(id=1)
        title = recipe.title
        self.assertEqual(title, "test")

    def test_get_recipe_ingredientsList(self):
        recipe = Recipe.objects.get(id=1)
        ingredientsList = recipe.ingredientsList
        self.assertEqual(ingredientsList, "ingredient 1")

    def test_get_recipe_directionsList(self):
        recipe = Recipe.objects.get(id=1)
        directionsList = recipe.directionsList
        self.assertEqual(directionsList, "This is step 1")
    
    def test_get_recipe_time(self):
        recipe = Recipe.objects.get(id=1)
        time = recipe.time
        self.assertEqual(time, 60)

    def test_get_recipe_dietaryRestrictions(self):
        recipe = Recipe.objects.get(id=1)
        dietaryRestrictions = recipe.dietaryRestrictions
        self.assertEqual(dietaryRestrictions, "")

    def test_get_recipe_servingSize(self):
        recipe = Recipe.objects.get(id=1)
        servingSize = recipe.servingSize
        self.assertEqual(servingSize, 4)

    def test_get_recipe_blurb(self):
        recipe = Recipe.objects.get(id=1)
        blurb = recipe.blurb
        self.assertEqual(blurb, "this is a recipe")

    def test_get_recipe_difficultyRating(self):
        recipe = Recipe.objects.get(id=1)
        difficultyRating = recipe.difficultyRating
        self.assertEqual(difficultyRating, 3)

    def test_get_recipe_createdBy(self):
        recipe = Recipe.objects.get(id=1)
        createdBy = recipe.createdBy
        self.assertEqual(createdBy, Profile.objects.get(pk=1))

    def test_get_recipe_favoritedBy(self):
        recipe = Recipe.objects.get(id=1)
        favoritedBy = recipe.favoritedBy
        self.assertEqual(favoritedBy.count(), 2)

    # def test_insert_basic_recipe(self):

    