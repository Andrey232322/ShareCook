from django.contrib import admin
from .models import Tag, Ingredient, Recipe, Favorite
# Register your models here.
admin.site.register(Tag)
admin.site.register(Ingredient)
admin.site.register(Recipe)
admin.site.register(Favorite)