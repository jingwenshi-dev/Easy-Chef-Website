from rest_framework.permissions import BasePermission

from userdata.models import *
from django.shortcuts import get_object_or_404


class UserDataPermission(BasePermission):
    def has_permission(self, request, view):
        rtid = view.kwargs.get('rtid')
        cid = view.kwargs.get('cid')
        lrid = view.kwargs.get('lrid')
        spid = view.kwargs.get('spid')

        if rtid:
            rating = get_object_or_404(Rating, pk=rtid)
            return rating.user == request.user

        elif cid:
            comment = get_object_or_404(Comment, pk=cid)
            return comment.user == request.user

        elif lrid:
            liked_recipe = get_object_or_404(LikedRecipe, pk=lrid)
            return liked_recipe.user == request.user

        elif spid:
            shopping_lst = get_object_or_404(ShoppingList, pk=spid)
            return shopping_lst.user == request.user

        return True
