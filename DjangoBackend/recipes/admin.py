from django.contrib import admin

from recipes.models import Recipe, Step, Ingredient, RecipeIngredient

# Register your models here.
admin.site.register(Recipe)
admin.site.register(Step)
admin.site.register(Ingredient)
admin.site.register(RecipeIngredient)
