from rest_framework.permissions import BasePermission
from django.shortcuts import get_object_or_404

from recipes.models import Recipe


class RecipePermission(BasePermission):
    """
    Permission class for create, update and delete a recipe
    """
    def has_permission(self, request, view):
        if uid := view.kwargs.get('uid'):
            return request.user.id == uid

        rid = view.kwargs.get('rid')
        recipe = get_object_or_404(Recipe, pk=rid)
        return request.user == recipe.user

