#from rest_framework import serializers


#from users.models import CustomUser, Subscription
# from resept.models import (
#     FavoriteRecipe,
#     Ingredient,
#     Recipes,
#     ShoppingCart,
#     Tag
# )
#
# class TagSerializer(serializers.ModelSerializer):
#
#     class Meta:
#         model = Tag
#         fields = (
#             'id',
#             'name',
#             'color',
#             'slug',
#         )
#
#
# class IngredientSerializer(serializers.ModelSerializer):
#
#     class Meta:
#         model = Ingredient
#         fields = (
#             'id',
#             'name',
#             'measurement_unit',
#         )
#
# class RecipesSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Recipes
#         fields = '__all__'