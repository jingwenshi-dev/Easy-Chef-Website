from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from recipes.serializers import *
from django.db.models import Count
from django.http import JsonResponse
from rest_framework import status
from itertools import chain



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
        created = user.recipes.all()
        rated = user.rated.all().values_list('recipe')
        commented = user.commented.all().values_list('recipe')
        liked = user.liked.all().values_list('recipe')
        favorited = user.favorited.all().values_list('recipe')
        interacted = chain(created, rated, liked, commented)
        return JsonResponse({'created': created, 'favorited': favorited, 'interacted': interacted}, safe=False, status=status.HTTP_200_OK)


class SearchByName(ListAPIView):
    """
    Search recipes by name, ingredients, or creator.
    Then filter by cuisine, diet, or cooking time if these parameters are given.
    Finally, rank the recipes by their ratings and likes.
    Note: You may want to use pagination.
    """
    serializer_class = RecipeSerializer

    def get_queryset(self):
        name = self.kwargs.get('name')
        cuisine = self.kwargs.get('cuisine')
        diet = self.kwargs.get('diet')
        time = self.kwargs.get('time')
        recipe_queue = Recipe.objects.filter(title__icontains=name, diet=diet, cuisine=cuisine, time=time)
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
        ingredient = self.kwargs.get('ingredient')
        cuisine = self.kwargs.get('cuisine')
        diet = self.kwargs.get('diet')
        time = self.kwargs.get('time')

        recipe_queue = Recipe.objects.all()
        recipe_queue = recipe_queue.filter(recipe__ingredient__name__icontains=ingredient, diet=diet, cuisine=cuisine, time=time)

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
        creator = self.kwargs.get('creator')
        cuisine = self.kwargs.get('cuisine')
        diet = self.kwargs.get('diet')
        time = self.kwargs.get('time')

        recipe_queue = Recipe.objects.all()

        recipe_queue = recipe_queue.filter(user__username__icontains=creator, diet=diet, cuisine=cuisine, time=time)

        return recipe_queue


class IngredientAutocomplete(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = IngredientSerializer

    def get_queryset(self):
        name = self.request.query_params.get('ingredient')
        return Ingredient.objects.filter(name__istartswith=name)


class DisplayShoppingList():
    """
    Return combined ingredients and corresponding combined amount with unit.
    """
    # TODO
    pass
