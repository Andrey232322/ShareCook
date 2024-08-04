import csv

from django.db.models import Sum
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from rest_framework import status, viewsets, exceptions
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.reverse import reverse
from resept.models import Tag, Ingredient, Recipe, ShoppingList, RecipeIngredient, Favorite
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from .serializers import TagSerializer, IngredientSerializer, RecipeSerializer, FavoriteAndShoppingSerializer
from rest_framework.permissions import IsAuthenticated




class TagViewSet(viewsets.ReadOnlyModelViewSet):
    """Вьюсет тега."""
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    pagination_class = None


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Ingredient.objects.all()
    permission_classes = [IsAuthenticatedOrReadOnly]
    serializer_class = IngredientSerializer
    #filter_backends = [IngredientSearchFilter]
    search_fields = ('^name',)
    pagination_class = None

class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    @action(detail=True, methods=['get'], url_path='get-link', url_name='get-link')
    def get_link(self, request, pk=None):
        recipe = self.get_object()
        short_link = f"https://foodgram.example.org/s/{recipe.pk}d0"
        return Response({'short-link': short_link})

    @action(detail=False, methods=['get'], url_path='download_shopping_cart', url_name='download_shopping_cart',
            permission_classes=[IsAuthenticated])
    def download_shopping_cart(self, request):
        shopping_list = RecipeIngredient.objects.filter(
            recipe__shopping_list__user=request.user
        ).values(
            'ingredient__name', 'ingredient__measurement_unit'
        ).annotate(ingredient_total=Sum('amount'))

        text = 'Список покупок:\n\n'
        for item in shopping_list:
            text += (
                f'{item["ingredient__name"]}: {item["ingredient_total"]} '
                f'{item["ingredient__measurement_unit"]}\n'
            )

        response = HttpResponse(text, content_type='text/plain')
        response['Content-Disposition'] = 'attachment; filename="shopping_list.txt"'
        return response

    @action(detail=True, methods=['post', 'delete'], url_path='shopping_cart', url_name='shopping_cart')
    def shopping_cart(self, request, pk=None):
        recipe = get_object_or_404(Recipe, pk=pk)
        if request.method == 'POST':
            if ShoppingList.objects.filter(user=request.user,
                                           recipe=recipe).exists():
                raise exceptions.ValidationError(
                    'Рецепт уже добавлен в список покупок.'
                )
            ShoppingList.objects.create(user=request.user, recipe=recipe)
            serializer = FavoriteAndShoppingSerializer(
                recipe, context={'request': request}
            )
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        elif request.method == "DELETE":
            if not ShoppingList.objects.filter(user=request.user,
                                               recipe=recipe).exists():
                raise exceptions.ValidationError(
                    'Рецепта нет в списке покупок.'
                )
            shopping_cart = get_object_or_404(
                ShoppingList,
                user=request.user,
                recipe=recipe
            )
            shopping_cart.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=True, methods=['post', 'delete'], url_path='favorite')
    def favorite(self, request, pk):
        recipe = get_object_or_404(Recipe, pk=pk)
        if request.method == "POST":
            if Favorite.objects.filter(user=request.user,
                                       recipe=recipe).exists():
                raise exceptions.ValidationError(
                    'Рецепт уже добавлен в избранное.'
                )
            Favorite.objects.create(user=request.user, recipe=recipe)
            serializer = FavoriteAndShoppingSerializer(
                recipe, context={'request': request}
            )
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        elif request.method == "DELETE":
            if not Favorite.objects.filter(user=request.user,
                                           recipe=recipe).exists():
                raise exceptions.ValidationError(
                    'Рецепта нет в избранном.'
                )
            favorite = get_object_or_404(
                Favorite,
                user=request.user,
                recipe=recipe
            )
            favorite.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)