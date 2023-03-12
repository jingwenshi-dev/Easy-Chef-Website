from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from recipes.serializers import *
from django.db.models import Count
from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework import status
from itertools import chain
from django.core import serializers
from userdata.models import ShoppingList


# Create your views here.
class PopularRecipes(ListAPIView):
    """
    Return a list of recipes based on its overall rating or the number of users marked them as favorite.
    Note: You may want to use pagination.
    """
    serializer_class = RecipeSerializer

    def get_queryset(self):
        recipes = Recipe.objects.annotate(num_likes=Count('liked')).order_by('-num_likes')
        return recipes


class MyRecipe(ListAPIView):
    """
    Return three list of recipes: Created, Liked, Interacted (create, like, rate, or comment)
    Note: You may want to use pagination.
    """
    permission_classes = [IsAuthenticated]
    serializer_class = RecipeSerializer

    def list(self, request):
        user = request.user
        created = user.created_recipe.all()
        created = serializers.serialize('json', created)
        rated = user.rated.all().values_list('recipe')
        commented = user.commented.all().values_list('recipe')
        liked = user.liked.all().values_list('recipe')
        favorited = user.favorited.all().values_list('recipe')
        interacted = chain(created, rated, liked, commented)
        return JsonResponse({'created': created, 'favorited': favorited, 'interacted': interacted}, safe=False,
                            status=status.HTTP_200_OK)


class SearchByName(ListAPIView):
    """
    Search recipes by name, ingredients, or creator.
    Then filter by cuisine, diet, or cooking time if these parameters are given.
    Finally, rank the recipes by their ratings and likes.
    Note: You may want to use pagination.
    """
    serializer_class = RecipeSerializer

    def get_queryset(self):
        name = self.request.query_params.get('name')
        cuisine = self.request.query_params.get('cuisine')
        diet = self.request.query_params.get('diet')
        time = self.request.query_params.get('time')
        time_unit = self.request.query_params.get('unit')
        recipe_queue = Recipe.objects.filter(title__icontains=name, diet__icontains=diet, cuisine__icontains=cuisine, time=time, time_unit__icontains=time_unit)
        recipe_queue = recipe_queue.annotate(num_likes=Count('liked')).order_by('-num_likes')
        return recipe_queue


class SearchByIngredient(ListAPIView):
    """
    Search recipes by name, ingredients, or creator.
    Then filter by cuisine, diet, or cooking time if these parameters are given.
    Finally, rank the recipes by their ratings and likes.
    Note: You may want to use pagination.
    """
    serializer_class = RecipeSerializer

    def get_queryset(self):
        ingredient = self.request.query_params.get('ingredient')
        cuisine = self.request.query_params.get('cuisine')
        diet = self.request.query_params.get('diet')
        time = self.request.query_params.get('time')
        time_unit = self.request.query_params.get('unit')

        recipe_queue = Recipe.objects.all()
        recipe_queue = recipe_queue.filter(recipe__ingredient__name__icontains=ingredient, diet__icontains=diet, cuisine__icontains=cuisine, time=time, time_unit__icontains=time_unit)
        recipe_queue = recipe_queue.annotate(num_likes=Count('liked')).order_by('-num_likes')

        return recipe_queue


class SearchByCreator(ListAPIView):
    """
    Search recipes by name, ingredients, or creator.
    Then filter by cuisine, diet, or cooking time if these parameters are given.
    Finally, rank the recipes by their ratings and likes.
    Note: You may want to use pagination.
    """
    serializer_class = RecipeSerializer

    def get_queryset(self):
        creator = self.request.query_params.get('creator')
        cuisine = self.request.query_params.get('cuisine')
        diet = self.request.query_params.get('diet')
        time = self.request.query_params.get('time')
        time_unit = self.request.query_params.get('unit')

        recipe_queue = Recipe.objects.all()

        recipe_queue = recipe_queue.filter(user__username__icontains=creator, diet__icontains=diet, cuisine__icontains=cuisine, time=time, time_unit__icontains=time_unit)
        recipe_queue = recipe_queue.annotate(num_likes=Count('liked')).order_by('-num_likes')

        return recipe_queue


class IngredientAutocomplete(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = IngredientSerializer

    def get_queryset(self):
        name = self.request.query_params.get('ingredient')
        return Ingredient.objects.filter(name__istartswith=name)


class DisplayShoppingList(APIView):
    """
    Return combined ingredients and corresponding combined amount with unit.
    """
    def get(self, request):
        user = request.user
        shopping_lst = ShoppingList.objects.filter(user=user)
        ingredient_lst = {}

        recipe_ingredient_lst = []

        for item in shopping_lst:
            recipe = item.recipe
            recipe_ingredients = RecipeIngredient.objects.filter(recipe=recipe)
            for recipe_ingredient in recipe_ingredients:
                recipe_ingredient_lst.append(recipe_ingredient)

        for recipe_ingredient in recipe_ingredient_lst:
            name = recipe_ingredient.ingredient.name
            amount = recipe_ingredient.amount
            unit = recipe_ingredient.unit

            if name in ingredient_lst:
                ingredient_lst[name]['amount'] += amount
            else:
                ingredient_lst[name] = {'amount': amount, 'unit': unit}

        return Response(data=ingredient_lst, status=200)



