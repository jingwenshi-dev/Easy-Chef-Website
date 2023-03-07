from django.db import models

from accounts.models import User


# Create your models here.
class Recipe(models.Model):

    user = models.ForeignKey(to=User, on_delete=models.CASCADE, related_name='creator', default=None)
    title = models.CharField(max_length=100)
    description = models.TextField(max_length=500)
    # A list of ingredients and steps will be stored as JSON object
    ingredients = models.JSONField()
    steps = models.JSONField()
    time = models.CharField(max_length=4)
    cuisine = models.CharField(max_length=15)
    diet = models.CharField(max_length=30)


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
