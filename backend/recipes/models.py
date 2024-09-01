from django.db import models
import os
import sys
sys.path.append(os.path.join(os.getcwd(), '..'))
from users.models import User


class Tag(models.Model):
    name = models.CharField(max_length=64, verbose_name='название')
    slug = models.CharField(max_length=64, unique=True)

    def __str__(self):
        return self.name
    class Meta:
        verbose_name = 'Ингридиент',
        verbose_name_plural = 'Ингридиенты'

class Ingredient(models.Model):
    name = models.CharField(max_length=128,verbose_name='название')
    measurement_unit = models.CharField(max_length=64)

    def __str__(self):
        return self.name
    class Meta:
        verbose_name = 'Тэг',
        verbose_name_plural = 'Тэги'

class Recipe(models.Model):
    tags = models.ManyToManyField(Tag, related_name='recipes')
    author = models.ForeignKey(User, related_name='recipes', on_delete=models.CASCADE)
    ingredients = models.ManyToManyField(Ingredient, related_name='recipes')
    is_favorited = models.BooleanField(default=False)
    is_in_shopping_cart = models.BooleanField(default=False)
    name = models.CharField(max_length=256,verbose_name='название')
    images = models.ImageField()
    text = models.CharField(max_length=256,)
    cooking_time = models.IntegerField()

    class Meta:
        ordering = ['author']

    def __str__(self):
        return self.name
    class Meta:
        verbose_name = 'Рецепте',
        verbose_name_plural = 'Рецепты'
class RecipeIngredient(models.Model):

    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='recipe_ingredients',
        verbose_name='Рецепт',
    )
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        related_name='ingredient_recipes',
        verbose_name='Ингредиент',
    )
    amount = models.PositiveSmallIntegerField(
        blank=False,
        verbose_name='Количество',
    )
    class Meta:
        verbose_name = 'Ингредиент в рецепте',
        verbose_name_plural = 'Ингредиент в рецепте'
class ShoppingList(models.Model):
    """Модель для добавления рецептов в корзину."""

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='shoppinglist',
        verbose_name='Владелец списка покупок',
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        null=True,
        related_name='shoppinglist',
        verbose_name='Рецепт из списка покупок',
    )

    class Meta:
        verbose_name = 'Список покупок'
        verbose_name_plural = 'Списки покупок'

class Favorite(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='favorites',
        verbose_name='Пользователь'
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='favorites',
        verbose_name='Рецепт'
    )

    class Meta:
        verbose_name = 'Избранное'
        verbose_name_plural = 'Избранное'