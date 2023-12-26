from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from .pagination import *
from recipes.serializers import *
from django.db.models import Count
from rest_framework import status
from rest_framework.response import Response
from userdata.models import ShoppingList


# Create your views here.
class PopularRecipes(ListAPIView):
    """
    Return a list of recipes based on its overall rating or the number of users marked them as favorite.
    Note: You may want to use pagination.
    """
    serializer_class = RecipeSerializer
    pagination_class = CustomPageNumberPagination

    def get_queryset(self):
        recipes = Recipe.objects.annotate(num_likes=Count('liked')).order_by('-num_likes')
        return recipes
    
class CreatedRecipe(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = RecipeSerializer
    pagination_class = CustomPageNumberPagination

    def get_queryset(self):
        user = self.request.user
        created_query = user.creator.all()
        return created_query

class FavoritedRecipe(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = RecipeSerializer
    pagination_class = CustomPageNumberPagination

    def get_queryset(self):
        user = self.request.user
        favorited_query = user.favorited.all()
        favorited = Recipe.objects.filter(id__in = favorited_query.values('recipe').distinct())
        return favorited

class InteractedRecipe(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = RecipeSerializer
    pagination_class = CustomPageNumberPagination

    def get_queryset(self):
        user = self.request.user
        created_query = user.creator.all()
        rated_query = user.rated.all()
        rated = Recipe.objects.filter(id__in = rated_query.values('recipe').distinct())
        commented_query = user.commented.all()
        commented = Recipe.objects.filter(id__in = commented_query.values('recipe').distinct())
        liked_query = user.liked.all()
        liked = Recipe.objects.filter(id__in = liked_query.values('recipe').distinct())
        interacted_query = created_query.union(rated, commented, liked)
        return interacted_query



class SearchByName(ListAPIView):
    """
    Search recipes by name, ingredients, or creator.
    Then filter by cuisine, diet, or cooking time if these parameters are given.
    Finally, rank the recipes by their ratings and likes.
    Note: You may want to use pagination.
    """
    serializer_class = RecipeSerializer
    pagination_class = CustomPageNumberPagination

    def get_queryset(self):
        name = self.request.query_params.get('name')
        cuisine = self.request.query_params.get('cuisine')
        diet = self.request.query_params.get('diet')
        time = self.request.query_params.get('time')
        time_unit = self.request.query_params.get('unit')

        if name:
            recipe_queue = Recipe.objects.filter(title__icontains=name)
            if cuisine:
                recipe_queue = recipe_queue.filter(cuisine__icontains=cuisine)
            if diet:
                recipe_queue = recipe_queue.filter(diet__icontains=diet)
            if time and time_unit:
                recipe_queue = recipe_queue.filter(time=time, time_unit__icontains=time_unit)

            recipe_queue = recipe_queue.annotate(num_likes=Count('liked')).order_by('-num_likes')
            return recipe_queue

        return None



class SearchByIngredient(ListAPIView):
    """
    Search recipes by name, ingredients, or creator.
    Then filter by cuisine, diet, or cooking time if these parameters are given.
    Finally, rank the recipes by their ratings and likes.
    Note: You may want to use pagination.
    """
    serializer_class = RecipeSerializer
    pagination_class = CustomPageNumberPagination

    def get_queryset(self):
        ingredient = self.request.query_params.get('ingredient')
        cuisine = self.request.query_params.get('cuisine')
        diet = self.request.query_params.get('diet')
        time = self.request.query_params.get('time')
        time_unit = self.request.query_params.get('unit')

        if ingredient:
            recipe_queue = Recipe.objects.filter(recipe__ingredient__name__icontains=ingredient)
            if cuisine:
                recipe_queue = recipe_queue.filter(cuisine__icontains=cuisine)
            if diet:
                recipe_queue = recipe_queue.filter(diet__icontains=diet)
            if time and time_unit:
                recipe_queue = recipe_queue.filter(time=time, time_unit__icontains=time_unit)

            recipe_queue = recipe_queue.annotate(num_likes=Count('liked')).order_by('-num_likes')
            return recipe_queue

        return None


class SearchByCreator(ListAPIView):
    """
    Search recipes by name, ingredients, or creator.
    Then filter by cuisine, diet, or cooking time if these parameters are given.
    Finally, rank the recipes by their ratings and likes.
    Note: You may want to use pagination.
    """
    serializer_class = RecipeSerializer
    pagination_class = CustomPageNumberPagination

    def get_queryset(self):
        creator = self.request.query_params.get('creator')
        cuisine = self.request.query_params.get('cuisine')
        diet = self.request.query_params.get('diet')
        time = self.request.query_params.get('time')
        time_unit = self.request.query_params.get('unit')

        if creator:
            recipe_queue = Recipe.objects.filter(user__username__icontains=creator)
            if cuisine:
                recipe_queue = recipe_queue.filter(cuisine__icontains=cuisine)
            if diet:
                recipe_queue = recipe_queue.filter(diet__icontains=diet)
            if time and time_unit:
                recipe_queue = recipe_queue.filter(time=time, time_unit__icontains=time_unit)

            recipe_queue = recipe_queue.annotate(num_likes=Count('liked')).order_by('-num_likes')
            return recipe_queue

        return None


class IngredientAutocomplete(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = IngredientSerializer

    def get_queryset(self):
        name = self.request.query_params.get('ingredient')
        if name:
            return Ingredient.objects.filter(name__istartswith=name)
        return None


class DisplayShoppingList(APIView):
    """
    Return combined ingredients and corresponding combined amount with unit.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        shopping_lst = ShoppingList.objects.filter(user=user)
        ingredient_lst = {}

        recipe_ingredient_lst = []

        for item in shopping_lst:
            recipe = item.recipe
            servings = item.number
            recipe_ingredients = RecipeIngredient.objects.filter(recipe=recipe)
            for recipe_ingredient in recipe_ingredients:
                recipe_ingredient_lst.append((recipe_ingredient, servings))

        for recipe_ingredient, servings in recipe_ingredient_lst:
            name = recipe_ingredient.ingredient.name
            amount = recipe_ingredient.amount
            unit = recipe_ingredient.unit

            if name in ingredient_lst:
                ingredient_lst[name]['amount'] += amount * servings
            else:
                ingredient_lst[name] = {'amount': amount * servings, 'unit': unit}

        return Response(data=ingredient_lst, status=200)



