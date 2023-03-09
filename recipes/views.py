from django.shortcuts import render, get_object_or_404
from rest_framework.exceptions import PermissionDenied
from rest_framework.generics import CreateAPIView, RetrieveAPIView
from rest_framework.permissions import IsAuthenticated, BasePermission

from accounts.models import User
from recipes.serializers import RecipeSerializer, StepSerializer, IngredientSerializer


# Create your views here.
class CreateRecipeView(CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = RecipeSerializer


class CreateStepView(CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = StepSerializer


class CreateIngredientView(CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = IngredientSerializer


class RecipeDetailView(RetrieveAPIView):
    pass
