from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination
from recipes.serializers import *
from django.db.models import Count
from rest_framework import status
from rest_framework.response import Response
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
    pagination_class = PageNumberPagination


    def list(self, request):
        user = request.user
        created_query = user.creator.all()
        created = [RecipeSerializer(recipe).data for recipe in created_query]
        rated_query = user.rated.all()
        rated = [RecipeSerializer(rate.recipe).data for rate in rated_query]
        commented_query = user.commented.all()
        commented = [RecipeSerializer(comment.recipe).data for comment in commented_query]
        liked_query = user.liked.all()
        liked = [RecipeSerializer(like.recipe).data for like in liked_query]
        favorited = user.favorited.all().values_list('recipe')
        interacted = created + rated + commented + liked
        interacted_distinct = [dict(t) for t in {tuple(d.items()) for d in interacted}]
        return Response({'created': created, 'favorited': favorited, 'interacted': interacted_distinct},
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


class DisplayShoppingList():
    """
    Return combined ingredients and corresponding combined amount with unit.
    """
    # TODO
    pass
