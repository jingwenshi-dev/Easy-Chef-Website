from django.db import models

from accounts.models import User


# Create your models here.
class Recipe(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.CASCADE, related_name='creator', default=None, null=False,
                             blank=False)
    title = models.CharField(max_length=100, null=False, blank=False)
    description = models.TextField(max_length=500, null=False, blank=False)
    picture = models.ImageField(upload_to='recipes/', blank=False, null=False)
    # A list of ingredients and steps will be stored as JSON object
    time = models.CharField(max_length=4, null=False, blank=False)
    time_unit = models.CharField(max_length=5, null=False, blank=False)
    cuisine = models.CharField(max_length=15, null=False, blank=False)
    diet = models.CharField(max_length=30, null=False, blank=False)


class Step(models.Model):
    recipe = models.ForeignKey(to=Recipe, on_delete=models.CASCADE, related_name='recipe_step', default=None, null=False, blank=False)
    description = models.TextField(null=False, blank=False)
    picture = models.ImageField(upload_to='recipes/')


class Ingredient(models.Model):
    recipe = models.ForeignKey(to=Recipe, on_delete=models.CASCADE, related_name='recipe_ingredient', default=None, null=False, blank=False)
    item = models.CharField(max_length=100, null=False, blank=False)
    unit = models.CharField(max_length=10, null=False, blank=False)


class Rating(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.CASCADE, related_name='user_rated', default=None)
    recipe = models.ForeignKey(to=Recipe, on_delete=models.CASCADE, related_name='recipe_rated', default=None)
    score = models.IntegerField()


class Comment(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.CASCADE, related_name='user_commented', default=None)
    recipe = models.ForeignKey(to=Recipe, on_delete=models.CASCADE, related_name='recipe_commented', default=None)
    message = models.TextField(max_length=500)


class LikedRecipe(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.CASCADE, related_name='user_liked', default=None)
    recipe = models.ForeignKey(to=Recipe, on_delete=models.CASCADE, related_name='recipe_liked', default=None)


class BrowsedRecipe(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.CASCADE, related_name='user_browsed', default=None)
    recipe = models.ForeignKey(to=Recipe, on_delete=models.CASCADE, related_name='recipe_browsed', default=None)


class ShoppingList(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.CASCADE, related_name='user_lst', default=None)
    recipe = models.ForeignKey(to=Recipe, on_delete=models.CASCADE, related_name='recipe_lst', default=None)
