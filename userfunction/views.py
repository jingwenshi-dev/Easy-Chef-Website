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


class MyRecipe(ListAPIView):
    """
    Return three list of recipes: Created, Liked, Interacted (create, like, rate, or comment)
    Note: You may want to use pagination.
    """
    permission_classes = [IsAuthenticated]
    serializer_class = RecipeSerializer
    pagination_class = CustomPageNumberPagination


    def list(self, request):
        user = request.user
        created_query = self.paginate_queryset(user.creator.all())
        created = [self.get_serializer(recipe).data for recipe in created_query]
        rated_query = self.paginate_queryset(user.rated.all())
        rated = [self.get_serializer(rate.recipe).data for rate in rated_query]
        commented_query = user.commented.all()
        commented = [self.get_serializer(comment.recipe).data for comment in commented_query]
        liked_query = user.liked.all()
        liked = [self.get_serializer(like.recipe).data for like in liked_query]
        favorited_query = self.paginate_queryset(user.favorited.all())
        favorited = [self.get_serializer(favorite.recipe).data for favorite in favorited_query]
        interacted = created + rated + commented + liked
        interacted_distinct = self.paginate_queryset([dict(t) for t in {tuple(d.items()) for d in interacted}])
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



