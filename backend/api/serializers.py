from django.core.exceptions import ValidationError
from djoser.serializers import UserCreateSerializer, UserSerializer
from rest_framework import serializers

from recipes.models import (Favorite, Ingredient, Recipe, RecipeIngredient,
                            ShoppingСart, Tag)
from users.models import Subscription, User
from .fields import Base64ImageField


MIN_PASSWORD_LENGTH = 5


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
    is_subscribed = serializers.SerializerMethodField()
    avatar = Base64ImageField()

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

    def get_is_subscribed(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return Subscription.objects.filter(user=request.user,
                                               author=obj).exists()
        return False


class AvatarUpdateSerializer(serializers.ModelSerializer):
    avatar = Base64ImageField()

    class Meta:
        model = User
        fields = ('avatar',)


class PasswordSerializer(serializers.Serializer):
    new_password = serializers.CharField(write_only=True, required=True)
    current_password = serializers.CharField(write_only=True, required=True)

    def validate(self, attrs):
        user = self.context['request'].user

        if not user.check_password(attrs['current_password']):
            raise ValidationError({'current_password': 'Неправильный пароль'})

        if len(attrs['new_password']) < MIN_PASSWORD_LENGTH:
            raise ValidationError("Пароль должен"
                                  " содержать минимум 5 символов.")

        return attrs


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


class RecipeIngredientGetSerializer(serializers.ModelSerializer):
    """Получение ингредиентов в рецепте."""

    id = serializers.IntegerField(source='ingredient.id')
    name = serializers.ReadOnlyField(source='ingredient.name')
    measurement_unit = serializers.ReadOnlyField(
        source='ingredient.measurements_unit'
    )

    class Meta:
        model = RecipeIngredient
        fields = ('id', 'name', 'measurement_unit', 'amount')


class RecipeSerializer(serializers.ModelSerializer):
    """Серилизатор для работы с тэгами."""
    author = UserReadSerializer(read_only=True)
    tags = TagSerializer(many=True)
    ingredients = RecipeIngredientGetSerializer(many=True,
                                                source='recipe_ingredients')
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()
    image = Base64ImageField(required=True, allow_null=False)

    class Meta:
        model = Recipe
        fields = ('id', 'tags', 'author', 'ingredients',
                  'is_in_shopping_cart', 'is_favorited', 'name',
                  'image', 'text', 'cooking_time',)

    def get_is_favorited(self, obj):
        """Проверяет, добавлен ли рецепт в избранное текущим пользователем."""
        user = self.context.get('request').user
        if user.is_authenticated:
            return Favorite.objects.filter(user=user, recipe=obj).exists()
        return False

    def get_is_in_shopping_cart(self, obj):
        user = self.context.get('request').user
        if user.is_authenticated:
            return ShoppingСart.objects.filter(user=user, recipe=obj).exists()
        return False


class IngredientAmountSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(source='ingredient.id')
    amount = serializers.IntegerField()

    class Meta:
        model = RecipeIngredient
        fields = ('id', 'amount')


class RecipeCreateSerializer(serializers.ModelSerializer):
    """Серилизатор для работы с тэгами."""
    image = Base64ImageField(required=True, allow_null=False)
    tags = serializers.PrimaryKeyRelatedField(queryset=Tag.objects.all(),
                                              many=True)
    ingredients = IngredientAmountSerializer(many=True)

    class Meta:
        model = Recipe
        fields = ('id', 'ingredients', 'tags',
                  'image', 'name', 'text', 'cooking_time',)

    def validate(self, data):
        if len(data['tags']) != len(set(data['tags'])):
            raise ValidationError('Теги должны быть уникальными.')

        ingredients = data.get('ingredients', [])
        ingredient_ids = [ingredient['ingredient']['id']
                          for ingredient in ingredients]

        if len(ingredient_ids) != len(set(ingredient_ids)):
            raise ValidationError('Ингредиенты должны быть уникальными.')

        return data

    def create_ingredients(self, ingredients_data, recipe):
        """
        Метод для создания ингредиентов для рецепта.
        Использует bulk_create для оптимизации.
        """
        recipe_ingredients = []
        for ingredient_data in ingredients_data:
            amount = ingredient_data['amount']
            ingredient_id = ingredient_data['ingredient']['id']
            recipe_ingredients.append(RecipeIngredient(
                recipe=recipe,
                ingredient_id=ingredient_id,
                amount=amount
            ))
        RecipeIngredient.objects.bulk_create(recipe_ingredients)

    def create(self, validated_data):
        """
        Создание нового рецепта с ингредиентами и тегами.
        """
        tags_data = validated_data.pop('tags')
        ingredients_data = validated_data.pop('ingredients')
        recipe = Recipe.objects.create(**validated_data)
        recipe.tags.set(tags_data)
        self.create_ingredients(ingredients_data, recipe)
        return recipe

    def update(self, instance, validated_data):
        """
        Обновление рецепта с ингредиентами и тегами.
        """
        tags_data = validated_data.pop('tags', None)
        ingredients_data = validated_data.pop('ingredients', None)
        instance = super().update(instance, validated_data)

        if tags_data:
            instance.tags.set(tags_data)

        if ingredients_data:
            RecipeIngredient.objects.filter(recipe=instance).delete()
            self.create_ingredients(ingredients_data, instance)

        return instance


class SubscriptionSerializer(serializers.ModelSerializer):
    recipes_count = serializers.IntegerField(
        source='recipes.count',
        read_only=True
    )
    recipes = RecipeSerializer(many=True)
    is_subscribed = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = User  # Модель пользователя
        fields = ('email', 'id', 'username', 'first_name',
                  'last_name', 'is_subscribed', 'recipes', 'recipes_count')

    def get_is_subscribed(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return Subscription.objects.filter(user=request.user,
                                               author=obj).exists()
        return False


class ShoppingCartSerializer(serializers.Serializer):
    """Добавление и удаление рецептов из корзины покупок."""
    pass


class FavoriteSerializer(serializers.ModelSerializer):
    image = Base64ImageField(required=True, allow_null=False)

    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time')
