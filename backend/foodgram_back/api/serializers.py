from rest_framework import serializers

from resept.models import (
    Recipe,
    Ingredient,
    Tag
)

from user.serializers import Base64ImageField


#
class TagSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tag
        fields = (
            'id',
            'name',
            'slug',
        )


class IngredientSerializer(serializers.ModelSerializer):

    class Meta:
        model = Ingredient
        fields = (
            'id',
            'name',
            'measurement_unit',
        )


class RecipeSerializer(serializers.ModelSerializer):
    author = serializers.HiddenField(default=serializers.CurrentUserDefault())
    image = Base64ImageField(required=True, allow_null=False)
    class Meta:
        model = Recipe
        fields = '__all__'

class FavoriteAndShoppingSerializer(serializers.ModelSerializer):
    image = Base64ImageField(required=True, allow_null=False)
    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time')