"""P2 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from userfunction.views import *

urlpatterns = [
    path('popular-recipes/', PopularRecipes.as_view()),
    path('autocomplete/ingredient=<str:name>/', IngredientAutocomplete.as_view()),
    path('autocomplete/', IngredientAutocomplete.as_view()),
    path('my-recipe/', MyRecipe.as_view()),
    path('search/name/', SearchByName.as_view()),
    path('search/ingredient/', SearchByIngredient.as_view()),
    path('search/creator/', SearchByCreator.as_view()),
    # path('shopping-list/', DisplayShoppingList.as_view())
]
