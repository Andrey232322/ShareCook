from django.core.validators import RegexValidator
from django.db import models
from user.models import User

class Tag(models.Model):
    name = models.CharField(
        max_length=255,
        null=False,
        blank=False,
        verbose_name='Название'
    )
    slug = models.CharField(
        max_length=50,
        null=False,
        blank=False,
        unique=True,
        verbose_name='Слаг',
        validators=[
            RegexValidator('^[-a-zA-Z0-9_]+$')
        ])

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'
class Ingredient(models.Model):
    name = models.CharField(
        max_length=255,
        null=False,
        blank=False,
        verbose_name='Название'
    )
    measurement_unit = models.CharField(verbose_name='Единица измерения', max_length=255,)

    class Meta:
        verbose_name = 'Ингридиент'
        verbose_name_plural = 'Ингридиенты'

class Recipe(models.Model):
    ingredients = models.ManyToManyField(
        Ingredient,
        related_name='recipes',
        verbose_name='Ингредиент',
        max_length=255,)
    tags = models.ManyToManyField(Tag, related_name='recipes',)
    image = models.ImageField(upload_to='avatars/',
                              blank=True, null=True,
                              verbose_name='Изображение',
                              default='avatars/default.jpg',)
    name = models.CharField(
        max_length=255,
        null=False,
        blank=False,
        verbose_name='Название'
    )
    text = models.CharField(verbose_name='Текст',max_length=255)
    cooking_time = models.IntegerField(verbose_name='Время приготовления',)
    author = models.ForeignKey(User,
                               on_delete=models.CASCADE,
                               related_name='recipes',
                               verbose_name='Автор рецепта')

    class Meta:
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'

class ShoppingList(models.Model):
    """Модель для добавления рецептов в корзину."""

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='shopping_list',
        verbose_name='Владелец списка покупок',
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        null=True,
        related_name='shopping_list',
        verbose_name='Рецепт из списка покупок',
    )

    class Meta:
        verbose_name = 'Список покупок'
        verbose_name_plural = 'Списки покупок'
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'recipe'],
                name='unique_recipe'
            ),
        ]

    def __str__(self):
        return f'Рецепт из корзины покупок {self.user}'

class RecipeIngredient(models.Model):
    """Модель для добавления ингредиентов в рецепте."""

    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='recipe_ingredients',
        verbose_name='Рецепт',
    )
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        related_name='recipe_ingredients',
        verbose_name='Ингредиент',
    )
    amount = models.PositiveSmallIntegerField(
        blank=False,
        verbose_name='Количество',
    )

    class Meta:
        verbose_name = 'Ингредиент в рецепте',
        verbose_name_plural = 'Ингредиенты в рецепте'


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
        verbose_name = 'Избранный рецепт'
        verbose_name_plural = 'Список избранных рецептов'
