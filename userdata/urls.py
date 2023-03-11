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
from userdata.views import *

urlpatterns = [
    path('create-rating/', CreateRatingView.as_view()),
    path('rating=<int:rtid>/RU-rating/', RURatingView.as_view()),

    path('recipe=<int:rid>/create-comment/', CreateCommentView.as_view()),
    path('recipe=<int:rid>&comment=<int:cid>/RUD-comment/', RUDCommentView.as_view()),

    path('recipe=<int:rid>/create-liked-recipe/', CreateLikedRecipeView.as_view()),
    path('liked-recipe=<int:lrid>/RD-liked-recipe/', RDLikedRecipeView.as_view()),

    path('recipe=<int:rid>/create-browsed-recipe/', CreateBrowsedRecipeView.as_view()),
    path('browsed-recipe=<int:brid>/RD-browsed-recipe/', RDBrowsedRecipeView.as_view())

]
