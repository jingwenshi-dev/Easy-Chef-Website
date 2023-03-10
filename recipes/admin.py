from django.contrib import admin

from recipes.models import Recipe, Step, Ingredient, RecipeIngredient, Rating, Comment, LikedRecipe, BrowsedRecipe, ShoppingList

# Register your models here.
admin.site.register(Recipe)
admin.site.register(Step)
admin.site.register(Ingredient)
admin.site.register(Rating)
admin.site.register(Comment)
admin.site.register(LikedRecipe)
admin.site.register(BrowsedRecipe)
admin.site.register(ShoppingList)
admin.site.register(RecipeIngredient)