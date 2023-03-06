from django.db import models
from django.contrib.auth.models import AbstractUser

from recipes.models import Recipe


# Create your models here.
class User(AbstractUser):
    phone = models.CharField(blank=True)
    email = models.EmailField(blank=False, null=False)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)


class Rating(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.CASCADE, related_name='user', default=None)
    recipe = models.ForeignKey(to=Recipe, on_delete=models.CASCADE, related_name='recipe', default=None)
    score = models.IntegerField()


class Comment(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.CASCADE, related_name='user', default=None)
    recipe = models.ForeignKey(to=Recipe, on_delete=models.CASCADE, related_name='recipe', default=None)
    message = models.TextField(max_length=500)


class Liked(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.CASCADE, related_name='user', default=None)
    recipe = models.ForeignKey(to=Recipe, on_delete=models.CASCADE, related_name='recipe', default=None)


class Browsed(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.CASCADE, related_name='user', default=None)
    recipe = models.ForeignKey(to=Recipe, on_delete=models.CASCADE, related_name='recipe', default=None)


class ShoppingList(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.CASCADE, related_name='user', default=None)
    recipe = models.ForeignKey(to=Recipe, on_delete=models.CASCADE, related_name='recipe', default=None)
