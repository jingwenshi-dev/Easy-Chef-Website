from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from recipes.serializers import *


# Create your views here.
class PopularRecipes():
    """
    Return a list of recipes based on its overall rating or the number of users marked them as favorite.
    Note: You may want to use pagination.
    """
    # TODO
    pass


class MyRecipe():
    """
    Return three list of recipes: Created, Liked, Interacted (create, like, rate, or comment)
    Note: You may want to use pagination.
    """
    # TODO
    pass


class Serach():
    """
    Search recipes by name, ingredients, or creator.
    Then filter by cuisine, diet, or cooking time if these parameters are given.
    Finally, rank the recipes by their ratings and likes.
    Note: You may want to use pagination.
    """
    # TODO
    pass


class IngredientAutocomplete(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = IngredientSerializer

    def get_queryset(self):
        name = self.kwargs.get('name')
        return Ingredient.objects.filter(name__startswith=name)


class DisplayShoppingList():
    """
    Return combined ingredients and corresponding combined amount with unit.
    """
    # TODO
    pass
