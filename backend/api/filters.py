# я не понимаю что ты хочешь чтобы я тут исправил по пепу
# Импорты из стандартных библиотек идут первыми.
# Затем идут сторонние библиотеки (например, django_filters).
# В конце следуют локальные импорты.
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
