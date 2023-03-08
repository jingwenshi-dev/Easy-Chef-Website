from django.shortcuts import render
from rest_framework.generics import CreateAPIView, RetrieveAPIView
from rest_framework.permissions import IsAuthenticated

from recipes.serializers import CreateRecipeSerializer


# Create your views here.
class CreateRecipeView(CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = CreateRecipeSerializer


class RecipeView(RetrieveAPIView):
    pass
