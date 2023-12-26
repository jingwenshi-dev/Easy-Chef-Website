from django.http import JsonResponse
from rest_framework.generics import CreateAPIView, RetrieveUpdateDestroyAPIView, RetrieveAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.exceptions import NotFound
from recipes.permissions import *
from userdata.serializers import *

"""
API Class Naming Convention:
For API classes with more than one functionality of CRUD, use letters for shorthand.
E.g. RUDStepView is responsible for Retrieve, Update and Delete of a Step instance only.
"""


class CreateRecipeView(CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = RecipeSerializer


class RecipeEditView(RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated, RecipeOwnershipPermission]
    serializer_class = RecipeSerializer

    def get_object(self):
        rid = self.kwargs.get("rid", "")
        recipe = get_object_or_404(Recipe, pk=rid)
        return recipe


class CreateStepView(CreateAPIView):
    permission_classes = [IsAuthenticated, RecipeOwnershipPermission]
    serializer_class = StepSerializer


class RUDStepView(RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated, RecipeOwnershipPermission]
    serializer_class = StepSerializer

    def get_object(self):
        sid = self.kwargs.get("sid", "")
        step = get_object_or_404(Step, pk=sid)
        return step


class CreateIngredientView(CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = IngredientSerializer


class RetrieveIngredientView(RetrieveAPIView):
    serializer_class = IngredientSerializer

    def get_object(self):
        name = self.request.query_params.get('ingredient')
        if name:
            query = Ingredient.objects.filter(name=name)
            if query.exists():
                return query[0]
        return None


class CreateRecipeIngredientView(CreateAPIView):
    """
    Create a unique combination of recipe and ingredient with a given amount and unit
    """
    permission_classes = [IsAuthenticated, RecipeOwnershipPermission]
    serializer_class = RecipeIngredientSerializer


class RUDRecipeIngredientView(RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated, RecipeOwnershipPermission]
    serializer_class = RecipeIngredientSerializer

    def get_object(self):
        """
        @return: A RecipeIngredient object based on the endpoint recipe and ingredient id.
        """
        rid = self.kwargs.get("rid", "")
        iid = self.kwargs.get("iid", "")

        recipe = get_object_or_404(Recipe, pk=rid)
        ingredient = get_object_or_404(Ingredient, pk=iid)

        recipe_ingredient = RecipeIngredient.objects.filter(recipe=recipe, ingredient=ingredient)

        if not recipe_ingredient.exists():
            raise NotFound(detail="The given combination of recipe and ingredient does not exist (Hint: Creat a new "
                                  "combination).")

        recipe_ingredient = recipe_ingredient[0]

        return recipe_ingredient


class RecipeDetailView(APIView):
    def get(self, request, rid):
        recipe = get_object_or_404(Recipe, id=rid)
        step = Step.objects.filter(recipe=recipe)
        recipe_ingredient = RecipeIngredient.objects.filter(recipe=recipe)
        comment = Comment.objects.filter(recipe=recipe)

        recipe_serializer = RecipeSerializer(recipe)
        step_serializer = StepSerializer(step, many=True)
        recipe_ingredient_serializer = RecipeIngredientSerializer(recipe_ingredient, many=True)
        if comment.exists():
            comment_serializer = CommentSerializer(comment, many=True)
            return JsonResponse(
                {"recipe": recipe_serializer.data, "step": step_serializer.data,
                 "recipe_ingredient": recipe_ingredient_serializer.data, "comment": comment_serializer.data})
        return JsonResponse(
            {"recipe": recipe_serializer.data, "step": step_serializer.data,
             "recipe_ingredient": recipe_ingredient_serializer.data, "comment": []})


class FetchRecipeView(APIView):
    permission_classes = [IsAuthenticated, RecipeOwnershipPermission]

    def get(self, request, rid):
        recipe = get_object_or_404(Recipe, id=rid)
        step = Step.objects.filter(recipe=recipe)
        recipe_ingredient = RecipeIngredient.objects.filter(recipe=recipe)
        comment = Comment.objects.filter(recipe=recipe)

        recipe_serializer = RecipeSerializer(recipe)
        step_serializer = StepSerializer(step, many=True)
        recipe_ingredient_serializer = RecipeIngredientSerializer(recipe_ingredient, many=True)
        if comment.exists():
            comment_serializer = CommentSerializer(comment, many=True)
            return JsonResponse(
                {"recipe": recipe_serializer.data, "step": step_serializer.data,
                 "recipe_ingredient": recipe_ingredient_serializer.data, "comment": comment_serializer.data})
        return JsonResponse(
            {"recipe": recipe_serializer.data, "step": step_serializer.data,
             "recipe_ingredient": recipe_ingredient_serializer.data, "comment": []})