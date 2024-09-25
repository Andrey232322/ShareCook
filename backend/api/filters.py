# Django Filter — это сторонняя библиотека, которая упрощает создание фильтров
# для моделей Django.
# django.contrib.auth относится к стандартным библиотекам фреймворка Django
# recipes.models моя, импорты локальных приложений или библиотек
# # Стандартная библиотека Django
# from django.contrib.auth import get_user_model
#
# # Сторонняя библиотека
# from django_filters import rest_framework as filters
#
# # Локальная библиотека
# from recipes.models import Recipe
# импорты разных категорий (стандартные библиотеки,
#                          сторонние библиотеки,
#                          локальные модули)
# разделены пустыми строками, как и предписано PEP 8.
from django.contrib.auth import get_user_model

from django_filters import rest_framework as filters

from recipes.models import Recipe


User = get_user_model()


class RecipeFilter(filters.FilterSet):

    is_favorited = filters.BooleanFilter(
        method='get_favorite',
        label='Избранные рецепты',
    )
    is_in_shopping_cart = filters.BooleanFilter(
        method='get_in_shopping_cart',
        label='В списке покупок',
    )

    class Meta:
        model = Recipe
        fields = (
            'is_favorited', 'is_in_shopping_cart',
        )

    def get_favorite(self, queryset, name, value):
        if value:
            return Recipe.objects.filter(favorited_by__user=self.request.user)
        return queryset

    def get_in_shopping_cart(self, queryset, name, value):
        if value:
            return Recipe.objects.filter(shopping_cart__user=self.request.user)
        return queryset
