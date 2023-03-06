from django.db import models

from accounts.models import User


# Create your models here.
class Recipe(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.CASCADE, related_name='user', default=None)
    title = models.CharField(max_length=100)
    description = models.TextField(max_length=500)
    # A list of ingredients and steps will be stored as JSON object
    ingredients = models.JSONField()
    steps = models.JSONField()
    time = models.CharField()
    cuisine = models.CharField()
    diet = models.CharField()
