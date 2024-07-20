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
# class Ingredient(models.Model):
#     name = models.CharField(
#         max_length=255,
#         null=False,
#         blank=False,
#         verbose_name='Название'
#     )
#     measurement_unit = models.CharField(verbose_name='Единица измерения', max_length=255,)
#
#     class Meta:
#         verbose_name = 'Ингридиент'
#         verbose_name_plural = 'Ингридиенты'
#
class Recipe(models.Model):
    #ingredients = models.ManyToManyField(Ingredient, related_name='recipes', verbose_name='Ингредиент', max_length=255,)
    tags = models.ManyToManyField(Tag, related_name='resept',)
    image = models.ImageField(upload_to='avatars/', blank=True, null=True, verbose_name='Изображение')
    name = models.CharField(
        max_length=255,
        null=False,
        blank=False,
        verbose_name='Название'
    )
    text = models.CharField(verbose_name='Текст',max_length=255)
    cooking_time = models.IntegerField(verbose_name='Время приготовления',)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='resept', verbose_name='Автор рецепта')

    class Meta:
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'

