from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from recipes.serializers import *
from django.db.models import Count


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
    # TODO
    pass


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
        # TODO
        pass


class SearchByCreator(ListAPIView):
    """
    Search recipes by name, ingredients, or creator.
    Then filter by cuisine, diet, or cooking time if these parameters are given.
    Finally, rank the recipes by their ratings and likes.
    Note: You may want to use pagination.
    """
    serializer_class = RecipeSerializer

    def get_queryset(self):
        # TODO
        pass


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
