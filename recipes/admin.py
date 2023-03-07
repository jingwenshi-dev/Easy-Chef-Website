from django.contrib import admin

from recipes.models import Recipe, Rating, Comment, LikedRecipe, BrowsedRecipe, ShoppingList

# Register your models here.
admin.site.register(Recipe)
admin.site.register(Rating)
admin.site.register(Comment)
admin.site.register(LikedRecipe)
admin.site.register(BrowsedRecipe)
admin.site.register(ShoppingList)
