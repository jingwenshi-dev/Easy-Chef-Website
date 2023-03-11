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
from django.contrib import admin
from django.urls import path
from recipes.views import *

urlpatterns = [
    path('user=<int:uid>/create-recipe/', CreateRecipeView.as_view()),
    path('recipe=<int:rid>/RUD-recipe/', RecipeEditView.as_view()),

    path('recipe=<int:rid>/create-step/', CreateStepView.as_view()),
    path('recipe=<int:rid>&step=<int:sid>/RUD-step/', RUDStepView.as_view()),

    path('recipe=<int:rid>/create-ingredient/', CreateIngredientView.as_view()),

    path('recipe=<int:rid>&ingredient=<int:iid>/create-recipe-ingredient/', CreateRecipeIngredientView.as_view()),
    path('recipe=<int:rid>&ingredient=<int:iid>/RUD-recipe-ingredient/', RUDRecipeIngredientView.as_view()),

    path('recipe=<int:rid>/details/', RecipeDetailView.as_view())
]
