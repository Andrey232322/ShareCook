from rest_framework import serializers

from resept.models import (
    Recipe,
    Ingredient,
    Tag
)

from user.serializers import Base64ImageField, UserSerializer

from user.models import User



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
    image = Base64ImageField(required=False, allow_null=False)
    class Meta:
        model = Recipe
        fields = '__all__'

    def validate(self, data):
        if not data.get('image'):
            data['image'] = 'avatars/default.jpg'  # Укажите путь к изображению по умолчанию
        return data

class FavoriteAndShoppingSerializer(serializers.ModelSerializer):
    image = Base64ImageField(required=False, allow_null=False)
    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time')

    def validate(self, data):
        if not data.get('image'):
            data['image'] = 'avatars/default.jpg'  # Укажите путь к изображению по умолчанию
        return data

class SubscriptionSerializer(UserSerializer):
    recipes = serializers.SerializerMethodField(read_only=True)
    recipes_count = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ("email", "id", "username", "first_name", "last_name",
                  "is_subscribed", "recipes", "recipes_count")

    def get_recipes(self, obj):
        request = self.context.get('request')
        limit = request.query_params.get('recipes_limit')
        recipes = Recipe.objects.filter(author=obj)
        if limit:
            recipes = recipes[:int(limit)]
        serializer = RecipeSerializer(recipes, many=True)
        return serializer.data

    def get_recipes_count(self, obj):
        return Recipe.objects.filter(author=obj).count()