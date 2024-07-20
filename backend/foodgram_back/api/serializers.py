from rest_framework import serializers

from resept.models import (
    Recipe,
    Tag
)
#
class TagSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tag
        fields = (
            'id',
            'name',
            'color',
            'slug',
        )
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

class RecipeSerializer(serializers.ModelSerializer):
    author = serializers.HiddenField(default=serializers.CurrentUserDefault())
    class Meta:
        model = Recipe
        fields = '__all__'

