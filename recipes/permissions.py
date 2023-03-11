from rest_framework.permissions import BasePermission
from django.shortcuts import get_object_or_404

from recipes.models import Recipe


class RecipePermission(BasePermission):
    """
    Permission class for create, update and delete a recipe
    """

    def has_permission(self, request, view):
        """
        If uid, then rid DNE => Create.
        If rid, then uid DNE => Update or Delete.
        @precondition: Refer to the endpoint parameters.
        @return: True or False.
        """

        uid = view.kwargs.get('uid')
        rid = view.kwargs.get('rid')

        # Check logged in user == endpoint user
        if uid:
            return request.user.id == uid

        # Check recipe ownership
        elif rid:
            recipe = get_object_or_404(Recipe, pk=rid)
            return request.user == recipe.user


class StepPermission(BasePermission):
    """
    Permission class for create, update, delete a step
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

