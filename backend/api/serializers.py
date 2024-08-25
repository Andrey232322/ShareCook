
from recipes.models import Ingredient, Tag, Recipe, ShoppingList
import base64
from django.shortcuts import get_object_or_404
from recipes.models import Recipe
from django.core.files.base import ContentFile
from djoser.serializers import UserCreateSerializer, UserSerializer
from rest_framework import serializers

from users.models import User

class Base64ImageField(serializers.ImageField):
    def to_internal_value(self, data):
        if isinstance(data, str) and data.startswith('data:image'):
            format, imgstr = data.split(';base64,')
            ext = format.split('/')[-1]
            data = ContentFile(base64.b64decode(imgstr), name='temp.' + ext)
        return super().to_internal_value(data)

class UserCreateSerializer(UserCreateSerializer):

    class Meta:
        model = User
        fields = (
            'email',
            'username',
            'first_name',
            'last_name',
            'password'
        )
class UserReadSerializer(UserSerializer):

    class Meta:
        model = User
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'is_subscribed',
            'avatar'
        )

class AvatarUpdateSerializer(serializers.ModelSerializer):
    avatar = Base64ImageField()

    class Meta:
        model = User
        fields = ('avatar',)

class PasswordSerializer(serializers.Serializer):
    new_password = serializers.CharField(write_only=True, required=True)
    current_password = serializers.CharField(write_only=True, required=True)

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





class IngredientSerializer(serializers.ModelSerializer):
    """Серилизатор для работы с ингридиентами."""
    class Meta:
        model = Ingredient
        fields = ('id', 'name', 'measurement_unit')


class TagSerializer(serializers.ModelSerializer):
    """Серилизатор для работы с тэгами."""
    class Meta:
        model = Tag
        fields = ('id', 'name', 'slug')
class RecipeSerializer(serializers.ModelSerializer):
    author = UserReadSerializer()
    # tags = TagSerializer(many=True)  развернутый ответ будет
    # ingredients = IngredientSerializer(many=True)
    class Meta:
        model = Recipe
        fields = (
            'id',
            'tags',
            'author',
            'ingredients',
            'is_favorited',
            'is_in_shopping_cart',
            'name',
            'images',
            'text',
            'cooking_time',
        )

class RecipeCreatePutSerializer(serializers.ModelSerializer):
    tags = serializers.PrimaryKeyRelatedField(many=True, queryset=Tag.objects.all())
    ingredients = serializers.PrimaryKeyRelatedField(many=True, queryset=Ingredient.objects.all())

    class Meta:
        model = Recipe
        fields = (
            'ingredients',
            'tags',
            # 'images',
            'name',
            'text',
            'cooking_time',
            'author',
        )
class ShortRecipeSerializer(serializers.ModelSerializer):
    """Серилизатор для краткого вывода рецептов."""

    image = Base64ImageField(required=True, allow_null=False)

    class Meta:
        model = Recipe
        fields = (
            'id',
            'name',
            'image',
            'cooking_time',
        )
class FavoriteAndShoppingSerializer(serializers.ModelSerializer):
    image = Base64ImageField(required=False, allow_null=False)
    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time')

    # def validate(self, data):
    #     if not data.get('image'):
    #         data['image'] = 'avatars/default.jpg'  # Укажите путь к изображению по умолчанию
    #     return data





