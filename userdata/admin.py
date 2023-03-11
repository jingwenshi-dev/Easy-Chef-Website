from django.contrib import admin

from userdata.models import Rating, Comment, LikedRecipe, BrowsedRecipe, ShoppingList

# Register your models here.
admin.site.register(Rating)
admin.site.register(Comment)
admin.site.register(LikedRecipe)
admin.site.register(BrowsedRecipe)
admin.site.register(ShoppingList)