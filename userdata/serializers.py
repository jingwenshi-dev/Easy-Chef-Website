from django.shortcuts import get_object_or_404
from rest_framework import serializers

from accounts.models import User
from recipes.models import Recipe
from userdata.models import Comment, Rating, LikedRecipe, BrowsedRecipe, ShoppingList
