from rest_framework.permissions import BasePermission
from django.shortcuts import get_object_or_404
from recipes.models import Recipe


class RecipeOwnershipPermission(BasePermission):
    """
    Permission class for the ownership of a Recipe instance
    @note: For create recipe and create ingredient, checking ownership of the recipe is redundant.
    """

    def has_permission(self, request, view):
        """
        Check the ownership of recipe.
        @precondition: Refer to the endpoint parameters.
        @return: True or False.
        """
        rid = view.kwargs.get('rid')
        recipe = get_object_or_404(Recipe, pk=rid)
        return request.user == recipe.user
