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
from recipes.views import CreateRecipeView, RecipeDetailView, CreateStepView, CreateIngredientView, CreateRecipeIngredientView, GetUpdateDestroyRecipeIngredientView, GetUpdateDestroyStepView

urlpatterns = [
    path('create-recipe/', CreateRecipeView.as_view()),
    path('<int:rid>/create-step/', CreateStepView.as_view()),
    path('<int:rid>/create-ingredient/', CreateIngredientView.as_view()),
    path('<int:rid>/<int:iid>/create-recipe-ingredient/', CreateRecipeIngredientView.as_view()),
    path('<int:riid>/get-update-destory-recipe-ingredient', GetUpdateDestroyRecipeIngredientView.as_view()),
    path('<int:sid>/get-update-destory-step', GetUpdateDestroyStepView.as_view()),
    path('<int:rid>/details/', RecipeDetailView.as_view())
]
