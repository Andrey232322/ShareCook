from django.contrib.auth import get_user_model
from django_filters import rest_framework as filters
import django_filters

from recipes.models import Recipe, Tag, Ingredient


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
    tags = django_filters.ModelMultipleChoiceFilter(
        field_name='tags',
        queryset=Tag.objects.all(),
        to_field_name='id',
    )
    author = django_filters.NumberFilter(field_name='author')

    class Meta:
        model = Recipe
        fields = (
            'is_favorited', 'is_in_shopping_cart', 'tags', 'author'
        )

    def get_favorite(self, queryset, name, value):
        if value:
            return Recipe.objects.filter(favorited_by__user=self.request.user)
        return queryset

    def get_in_shopping_cart(self, queryset, name, value):
        if value:
            return Recipe.objects.filter(shopping_cart__user=self.request.user)
        return queryset


class IngredientFilter(filters.FilterSet):

    name = filters.CharFilter(
        field_name='name',
    )

    class Meta:
        model = Ingredient
        fields = ('name',)
