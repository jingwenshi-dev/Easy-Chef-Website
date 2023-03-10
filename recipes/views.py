from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from rest_framework.exceptions import PermissionDenied
from rest_framework.generics import CreateAPIView, RetrieveAPIView, ListAPIView, ListCreateAPIView
from rest_framework.permissions import IsAuthenticated, BasePermission
from rest_framework.views import APIView
from rest_framework.response import Response

from accounts.models import User
from recipes.models import Recipe, Step, Ingredient, RecipeIngredient
from recipes.serializers import RecipeSerializer, StepSerializer, IngredientSerializer, RecipeIngredientSerializer


# Create your views here.
class CreateRecipeView(CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = RecipeSerializer


class CreateStepView(CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = StepSerializer


#
# class GetCreateUpdateIngredientView(APIView):
#     """
#     Get the list of ingredient with all corresponding fields and ID.
#     If any ingredient DNE, create one it first.
#     """
#
#     def post(self, request, *args, **kwargs):
#
#         # Get current recipe
#         rid = self.kwargs.get("rid")
#         recipe = get_object_or_404(Recipe, rid)
#
#         # Get list of input ingredient in JSON
#         items = request.data.get('items', [])
#
#         lst = []
#
#         for item in items:
#
#             field_empty_err = []
#
#             name = item.get('name', '')
#             amount = item.get('amount', '')
#             unit = item.get('unit', '')
#
#             if name == '':
#                 errors = {"item": field_empty_err}
#
#         for item in items:
#             name = item.get('name', '')
#             amount = item.get('amount', '')
#             unit = item.get('unit', '')
#
#             # Get the ingredient, or create the ingredient if DNE
#             ingredient, created = Ingredient.objects.get_or_create(name=name)
#
#             # Link ingredient with recipe, or create that relation if DNE
#             recipe_ingredient, created = RecipeIngredient.objects.update_or_create(recipe=recipe, ingredient=ingredient,
#                                                                                    amount=amount, unit=unit)
#
#             lst.append({"id": pk, "name": name})
#
#         return JsonResponse({"items": lst})


class GetOrCreateIngredientView(CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = IngredientSerializer

    def perform_create(self, serializer):
        instance = serializer.save()
        serialized_data = self.serializer_class(instance).data
        return Response(serialized_data, status=201)


class CreateOrUpdateIngredientView(CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = RecipeIngredientSerializer


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
