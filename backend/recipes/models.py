from django.db import models
from users.models import User


class Tag(models.Model):
    name = models.CharField(max_length=64, verbose_name='название')
    slug = models.CharField(max_length=64, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Тэг',
        verbose_name_plural = 'Тэг'


class Ingredient(models.Model):

    name = models.CharField(max_length=128, verbose_name='название')
    measurement_unit = models.CharField(max_length=64)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Ингридиент',
        verbose_name_plural = 'Ингридиенты'


class Recipe(models.Model):
    tags = models.ManyToManyField(Tag, related_name='recipes')
    author = models.ForeignKey(User,
                               related_name='recipes',
                               on_delete=models.CASCADE)
    ingredients = models.ManyToManyField(Ingredient, related_name='recipes')
    name = models.CharField(max_length=256, verbose_name='название')
    image = models.ImageField(upload_to='recipes/',)
    text = models.CharField(max_length=256,)
    cooking_time = models.IntegerField()

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['author']
        verbose_name = 'Рецепте',
        verbose_name_plural = 'Рецепты'


class RecipeIngredient(models.Model):
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='recipe_ingredients',  # связь с рецептом
        verbose_name='Рецепт',
    )
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        related_name='ingredient_recipes',  # связь с ингредиентом
        verbose_name='Ингредиент',
    )
    amount = models.PositiveSmallIntegerField(
        blank=False,
        verbose_name='Количество',
    )

    class Meta:
        verbose_name = 'Ингредиент в рецепте',
        verbose_name_plural = 'Ингредиент в рецепте'


class ShoppingСart(models.Model):
    """Модель для добавления рецептов в корзину."""

    user = models.ForeignKey(User,
                             on_delete=models.CASCADE,
                             related_name='shopping_cart')
    recipe = models.ForeignKey(Recipe,
                               on_delete=models.CASCADE,
                               related_name='shopping_cart')

    class Meta:
        verbose_name = 'Список покупок'
        verbose_name_plural = 'Списки покупок'


class Favorite(models.Model):

    user = models.ForeignKey(User,
                             on_delete=models.CASCADE,
                             related_name='favorites')
    recipe = models.ForeignKey(Recipe,
                               on_delete=models.CASCADE,
                               related_name='favorited_by')

    class Meta:
        verbose_name = 'Избранное'
        verbose_name_plural = 'Избранное'
