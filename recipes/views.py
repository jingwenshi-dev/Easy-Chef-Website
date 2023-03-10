from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from rest_framework.exceptions import PermissionDenied
from rest_framework.generics import CreateAPIView, RetrieveAPIView, ListAPIView, ListCreateAPIView
from rest_framework.permissions import IsAuthenticated, BasePermission
from rest_framework.views import APIView
from rest_framework.response import Response

from accounts.models import User
from recipes.models import Recipe, Step, Ingredient
from recipes.serializers import RecipeSerializer, StepSerializer


# Create your views here.
class CreateRecipeView(CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = RecipeSerializer


class CreateStepView(CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = StepSerializer


class GetOrCreateIngredientView(CreateAPIView):
    """
    Get the list of ingredient with all corresponding fields and ID.
    If any ingredient DNE, create one it first.
    """
    def post(self, request, *args, **kwargs):
        items = request.data.get('items', [])

        lst = []

        for item in items:
            ingredient, created = Ingredient.objects.get_or_create(item=item.get('item', ''))

            pk = ingredient.pk
            item = ingredient.item

            lst.append({"id": pk, "item": item})

        return JsonResponse({"items": lst})


class RecipeDetailView(APIView):
    def get(self, request, rid):
        recipe = get_object_or_404(Recipe, id=rid)
        step = Step.objects.filter(recipe=recipe)
        ingredient = Ingredient.objects.filter(recipe=recipe)

        recipe_serializer = RecipeSerializer(recipe)
        step_serializer = StepSerializer(step, many=True)
        ingredient_serializer = IngredientSerializer(ingredient, many=True)

        return JsonResponse(
            {"recipe": recipe_serializer.data, "step": step_serializer.data, "ingredient": ingredient_serializer.data})
