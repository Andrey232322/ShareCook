<<<<<<< HEAD
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, validate_slug
from django.db import models

User = get_user_model()


class Ingredient(models.Model):
    '''Модель ингредиентов.'''

    name = models.CharField(
        'Название ингредиента',
        max_length=200,
        blank=False,
    )
    measurement_unit = models.CharField(
        max_length=200,
        blank=False,
        verbose_name='Единицы измерения',
    )

    class Meta:
        ordering = ('name',)
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'

    def __str__(self):
        return self.name


class Tag(models.Model):
    '''Модель тэгов.'''

    name = models.CharField(
        'Название тэга',
        max_length=200,
        blank=False,
        unique=True,
    )
    slug = models.SlugField(
        'Слаг тэга',
        unique=True,
        blank=False,
        validators=[
            validate_slug
        ],
    )

    class Meta:
        verbose_name = 'Тэг'
        verbose_name_plural = 'Тэги'
=======
from django.db import models
from users.models import User


class Tag(models.Model):
    name = models.CharField(max_length=64, verbose_name='название')
    slug = models.CharField(max_length=64, unique=True)
>>>>>>> work

    def __str__(self):
        return self.name

<<<<<<< HEAD

class Recipe(models.Model):
    """Модель рецептов."""

    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        blank=False,
        related_name='recipes',
        verbose_name='Автор рецепта',
    )
    name = models.CharField(
        'Название рецепта',
        max_length=200,
        blank=False,
        help_text='Введите название рецепта',
    )
    text = models.TextField(
        'Описание рецепта',
        blank=False,
        help_text='Введите описание рецепта',
    )
    image = models.ImageField(
        'Изображение',
        upload_to='recipes/',
        blank=False,
        help_text='Прикрепите изображение',
    )
    ingredients = models.ManyToManyField(
        Ingredient,
        blank=False,
        related_name='recipes',
        verbose_name='Ингредиенты',
        help_text='Выберите ингредиенты',
    )
    tags = models.ManyToManyField(
        Tag,
        blank=False,
        related_name='recipes',
        verbose_name='Тэги',
        help_text='Выберите тэги',
    )
    cooking_time = models.PositiveSmallIntegerField(
        'Время приготовления',
        blank=False,
        validators=[
            MinValueValidator(
                1,
                'Время приготовления должно быть больше 1'
            )
        ],
        help_text='Время приготовления в минутах',
    )
    pub_date = models.DateTimeField(
        'Дата публикации',
        auto_now_add=True,
    )

    class Meta:
        ordering = ('-pub_date', )
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'
=======
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
>>>>>>> work

    def __str__(self):
        return self.name

<<<<<<< HEAD

class RecipeIngredient(models.Model):
    """Модель для добавления ингредиентов в рецепте."""

    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='recipe_ingredients',
=======
    class Meta:
        ordering = ['author']
        verbose_name = 'Рецепте',
        verbose_name_plural = 'Рецепты'


class RecipeIngredient(models.Model):
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='recipe_ingredients',  # связь с рецептом
>>>>>>> work
        verbose_name='Рецепт',
    )
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
<<<<<<< HEAD
        related_name='ingredient_recipes',
=======
        related_name='ingredient_recipes',  # связь с ингредиентом
>>>>>>> work
        verbose_name='Ингредиент',
    )
    amount = models.PositiveSmallIntegerField(
        blank=False,
        verbose_name='Количество',
    )

    class Meta:
        verbose_name = 'Ингредиент в рецепте',
<<<<<<< HEAD
        verbose_name_plural = 'Ингредиенты в рецепте'


class FavoritesList(models.Model):
    """Модель подписок."""

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='user_favorites',
        verbose_name='Владелец списка избранных рецептов',
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        null=True,
        related_name='favorites',
        verbose_name='Избранные рецепты',
    )

    class Meta:
        verbose_name = 'Список избранных рецептов'
        verbose_name_plural = 'Списки избранных рецептов'

    def __str__(self):
        return f'Избранный рецепт {self.user}'


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
=======
        verbose_name_plural = 'Ингредиент в рецепте'


class ShoppingСart(models.Model):
    """Модель для добавления рецептов в корзину."""

    user = models.ForeignKey(User,
                             on_delete=models.CASCADE,
                             related_name='shopping_cart')
    recipe = models.ForeignKey(Recipe,
                               on_delete=models.CASCADE,
                               related_name='shopping_cart')
>>>>>>> work

    class Meta:
        verbose_name = 'Список покупок'
        verbose_name_plural = 'Списки покупок'

<<<<<<< HEAD
    def __str__(self):
        return f'Рецепт из корзины покупок {self.user}'
=======

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
>>>>>>> work
