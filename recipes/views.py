from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from rest_framework.exceptions import PermissionDenied
from rest_framework.generics import CreateAPIView, RetrieveAPIView, ListAPIView
from rest_framework.permissions import IsAuthenticated, BasePermission
from rest_framework.views import APIView

from accounts.models import User
from recipes.models import Recipe, Step, Ingredient
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


class RecipeDetailView(APIView):
    def get(self, request, rid):
        recipe = get_object_or_404(Recipe, id=rid)
        step = Step.objects.filter(recipe=recipe)
        ingredient = Ingredient.objects.filter(recipe=recipe)

        recipe_serializer = RecipeSerializer(recipe)
        step_serializer = StepSerializer(step, many=True)
        ingredient_serializer = IngredientSerializer(ingredient, many=True)

        return JsonResponse({"recipe": recipe_serializer.data, "step": step_serializer.data, "ingredient": ingredient_serializer.data})
        # return JsonResponse({"recipe": recipe_serializer.data})
