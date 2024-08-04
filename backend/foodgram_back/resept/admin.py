from django.contrib import admin
from .models import Tag, Ingredient, Recipe, Favorite, RecipeIngredient
# Register your models here.
admin.site.register(Tag)
admin.site.register(Ingredient)
admin.site.register(Recipe)
admin.site.register(Favorite)
admin.site.register(RecipeIngredient)