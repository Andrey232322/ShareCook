import os
import sys
from django.http import HttpResponse
from django.db.models import Sum
from django.shortcuts import render
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework import viewsets, status, exceptions
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticatedOrReadOnly
#sys.path.append(os.path.join(os.getcwd(), '..'))
from recipes.models import Recipe, Ingredient, Tag, RecipeIngredient, ShoppingList, Favorite
from .serializers import IngredientSerializer, TagSerializer, RecipeCreatePutSerializer, RecipeSerializer, FavoriteAndShoppingSerializer, ShortRecipeSerializer
from django.shortcuts import get_object_or_404

class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    """Получение списка ингридиентов."""

    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer



class TagViewSet(viewsets.ReadOnlyModelViewSet):
    """Получение списка тэгов."""

    queryset = Tag.objects.all()
    serializer_class = TagSerializer


# Create your views here.
class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    permission_classes = (IsAuthenticatedOrReadOnly,)
    #pagination = PageNumberPagination

    def get_serializer_class(self):
        if self.action in ['create', 'update']:
            return RecipeCreatePutSerializer
        if self.action in ['favorite']:
            return ShortRecipeSerializer
        return RecipeSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    @action(detail=True, methods=['get'])
    def get_link(self, request, pk=None):
        recipe = self.get_object()
        short_link = f"https://random-foodgram.zapto.org/s/{recipe.pk}d0"
        return Response({'short-link': short_link})

    @action(detail=True, methods=['post', 'delete'])
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


    @action(detail=False, methods=['get'])
    def download_shopping_cart(self, request):
        shopping_list = RecipeIngredient.objects.filter(
            recipe__shoppinglist__user=request.user
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
        response['Content-Disposition'] = ('attachment; '
                                           'filename="shopping_list.txt"')
        return response

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



















