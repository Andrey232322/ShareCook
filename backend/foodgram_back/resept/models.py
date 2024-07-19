# from django.core.validators import RegexValidator
# from django.db import models
# from django.contrib.auth import get_user_model
# User = get_user_model()
#
#
# class Tag(models.Model):
#     name = models.CharField(
#         max_length=255,
#         null=False,
#         blank=False,
#         verbose_name='Название'
#     )
#     slug = models.CharField(
#         max_length=50,
#         null=False,
#         blank=False,
#         unique=True,
#         verbose_name='Слаг',
#         validators=[
#             RegexValidator('^[-a-zA-Z0-9_]+$')
#         ])
#
#     class Meta:
#         verbose_name = 'Тег'
#         verbose_name_plural = 'Теги'
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
# class Recipes(models.Model):
#     ingredients = models.ManyToManyField(Ingredient, related_name='recipes', verbose_name='Ингредиент', max_length=255,)
#     tags = models.ManyToManyField(Tag, related_name='resept',)
#     image = models.ImageField(upload_to='avatars/', blank=True, null=True, verbose_name='Изображение')
#     name = models.CharField(
#         max_length=255,
#         null=False,
#         blank=False,
#         verbose_name='Название'
#     )
#     text = models.CharField(verbose_name='Текст',max_length=255)
#     cooking_time = models.IntegerField(verbose_name='Время приготовления',)
#     author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='resept', verbose_name='Автор рецепта')
#
#     class Meta:
#         verbose_name = 'Рецепт'
#         verbose_name_plural = 'Рецепты'
#
#
# class CommonUserRecipeModel(models.Model):
#
#     user = models.ForeignKey(
#         User,
#         on_delete=models.CASCADE,
#         verbose_name='Пользователь'
#     )
#
#     recipe = models.ForeignKey(
#         Recipes,
#         on_delete=models.CASCADE,
#         verbose_name='Рецепт'
#     )
#
#     class Meta:
#         abstract = True
#         ordering = ['name']
#         constraints = [
#             models.UniqueConstraint(
#                 fields=['user', 'recipe'],
#                 name='unique_user_recipe',
#             )
#         ]
#
#
# class FavoriteRecipe(CommonUserRecipeModel):
#
#     class Meta:
#         verbose_name = 'Избранный рецепт'
#         verbose_name_plural = 'Избранные рецепты'
#
#
#     def __str__(self):
#         return f'Избранные рецепты {self.user}'
#
#
# class ShoppingCart(CommonUserRecipeModel):
#
#     class Meta:
#         verbose_name = 'Список покупок'
#         verbose_name_plural = 'Списки покупок'
#
#
#     def __str__(self):
#         return f'Список покупок {self.user}'