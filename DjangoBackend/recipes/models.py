from django.db import models
from accounts.models import User
from django.utils import timezone

# Create your models here.
class Recipe(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.CASCADE, related_name='creator', default=None,
                             blank=False)
    title = models.CharField(max_length=100, blank=False)
    description = models.TextField(max_length=500, blank=False)
    picture = models.ImageField(upload_to='recipes/', blank=False)
    # A list of ingredients and steps will be stored as JSON object
    time = models.CharField(max_length=4, blank=False)
    time_unit = models.CharField(max_length=5, blank=False)
    cuisine = models.CharField(max_length=15, blank=False)
    diet = models.CharField(max_length=30, blank=False)
    createdDate = models.DateTimeField(default=timezone.now)


class Step(models.Model):
    recipe = models.ForeignKey(to=Recipe, on_delete=models.CASCADE, related_name='steps', default=None, blank=False)
    number = models.IntegerField(blank=False)
    description = models.TextField(blank=False)
    picture = models.ImageField(upload_to='recipes/')


class Ingredient(models.Model):
    name = models.CharField(max_length=100, blank=False, unique=True)


class RecipeIngredient(models.Model):
    recipe = models.ForeignKey(to=Recipe, on_delete=models.CASCADE, related_name='recipe', default=None, blank=False)
    ingredient = models.ForeignKey(to=Ingredient, on_delete=models.CASCADE, related_name='ingredient', default=None, blank=False)
    amount = models.FloatField()
    unit = models.CharField(max_length=10)
