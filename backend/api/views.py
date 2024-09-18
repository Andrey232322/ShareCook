import base64
import mimetypes
from django.core.exceptions import ValidationError
from django.http import HttpResponse
from django.db.models import Sum
from rest_framework.exceptions import NotAuthenticated
from rest_framework.response import Response
from rest_framework import viewsets, status, exceptions
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticatedOrReadOnly, AllowAny, IsAuthenticated
from django.core.files.storage import default_storage
from recipes.models import Recipe, Ingredient, Tag, RecipeIngredient, ShoppingСart, Favorite
from .serializers import (UserCreateSerializer,
                          UserReadSerializer,
                          PasswordSerializer,
                          AvatarUpdateSerializer,
                          SubscriptionSerializer,
                          SubscribeSerializer,
                          IngredientSerializer,TagSerializer,
                          RecipeSerializer,
                          RecipeCreateSerializer,
                          ShoppingCartSerializer,
                          FavoriteSerializer,)
from django.shortcuts import get_object_or_404
from users.models import User, Subscription
from .filters import RecipeFilter


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    """Получение списка ингридиентов."""

    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    permission_classes = (AllowAny,)
    pagination_class = None


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    """Получение списка тэгов."""

    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = (AllowAny,)
    pagination_class = None


class UserViewSet(viewsets.ModelViewSet):

    queryset = User.objects.all()
    permission_classes = (AllowAny,)

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve', 'me'):
            return UserReadSerializer
        elif self.action == 'avatar':
            return AvatarUpdateSerializer
        elif self.action == 'set_password':
            return PasswordSerializer
        elif self.action == 'subscriptions':
            return SubscriptionSerializer
        elif self.action == 'subscribe':
            return SubscribeSerializer

        return UserCreateSerializer

    @action(detail=False, methods=['get'], url_path='me', permission_classes=(IsAuthenticated,))
    def me(self, request):
        serializer = self.get_serializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=['put', 'patch', 'delete'],
            url_path='me/avatar',
            serializer_class=AvatarUpdateSerializer)
    def avatar(self, request):
        user = request.user
        if request.method == 'DELETE':
            user.avatar.delete()
            user.avatar = None
            user.save()
            return Response(status=status.HTTP_204_NO_CONTENT)
        elif request.method in ['PUT', 'PATCH']:
            serializer = self.get_serializer(user,
                                             data=request.data, partial=True)
            try:
                serializer.is_valid(raise_exception=True)
                serializer.save()

                if user.avatar:
                    file_path = user.avatar.path
                    mime_type, _ = mimetypes.guess_type(file_path)
                    with default_storage.open(file_path, 'rb') as image_file:
                        image_data = image_file.read()
                        encoded_image = base64.b64encode(image_data).decode(
                            'utf-8')
                        avatar_data = (f"data:{mime_type};"
                                       f"base64,{encoded_image}")
                else:
                    avatar_data = None

                response_data = serializer.data
                response_data['avatar'] = avatar_data

                return Response(response_data, status=status.HTTP_200_OK)
            except ValidationError as e:
                required_fields = [field for field in serializer.fields
                                   if serializer.fields[field].required]
                error_response = {
                    "detail": "Validation error",
                    "errors": e.detail,
                    "required_fields": required_fields
                }
                return Response(error_response,
                                status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['post'], url_path='set_password')
    def set_password(self, request):
        user = request.user
        serializer = PasswordSerializer(data=request.data)
        if serializer.is_valid():
            if not user.check_password(serializer.validated_data['current_password']):
                return Response({'current_password': 'Неправильный пароль'}, status=status.HTTP_400_BAD_REQUEST)
            user.set_password(serializer.validated_data['new_password'])
            user.save()
            return Response({'status': 'Пароль изменён успешно'})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    @action(detail=False, methods=['get'], url_path='subscriptions', url_name='subscriptions')
    def subscriptions(self, request):
        user = self.request.user
        if not user.is_authenticated:
            raise NotAuthenticated("Вы должны войти в систему, чтобы просматривать подписки.")
        subscriptions = User.objects.filter(
            subscribing__user=user
        ).prefetch_related('recipes')

        paginated_queryset = self.paginate_queryset(subscriptions)
        if paginated_queryset is not None:
            serializer = self.get_serializer(paginated_queryset, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(subscriptions, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['post', 'delete'],
            serializer_class=SubscribeSerializer)
    def subscribe(self, request, pk=None):
        user = self.request.user
        author = get_object_or_404(User, pk=pk)

        if self.request.method == 'POST':
            if user == author:
                raise exceptions.ValidationError(
                    'Нельзя подписаться на самого себя!'
                )
            if Subscription.objects.filter(
                    user=user,
                    author=author
            ).exists():
                raise exceptions.ValidationError(
                    'Вы уже подписаны на этого автора.'
                )
            Subscription.objects.create(user=user, author=author)
            serializer = self.get_serializer(author)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        if self.request.method == 'DELETE':
            if not Subscription.objects.filter(
                    user=user,
                    author=author
            ).exists():
                raise exceptions.ValidationError(
                    'Подписка не была оформлена, либо уже удалена.'
                )
            subscription = get_object_or_404(
                Subscription,
                user=user,
                author=author
            )
            subscription.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)






class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    permission_classes = (IsAuthenticatedOrReadOnly,)
    filterset_class = RecipeFilter

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve'):
            return RecipeSerializer
        return RecipeCreateSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


    @action(detail=True, methods=['get'], url_path='get-link')
    def get_link(self, request, pk=None):
        recipe = self.get_object()
        short_link = f"https://random-foodgram.zapto.org/s/{recipe.pk}d0"
        return Response({'short-link': short_link})

    @action(detail=True, methods=['post', 'delete'])
    def shopping_cart(self, request, pk=None):
        recipe = get_object_or_404(Recipe, pk=pk)
        if request.method == 'POST':
            if ShoppingСart.objects.filter(user=request.user,
                                           recipe=recipe).exists():
                raise exceptions.ValidationError(
                    'Рецепт уже добавлен в список покупок.'
                )
            ShoppingСart.objects.create(user=request.user, recipe=recipe)
            serializer = ShoppingCartSerializer(
                recipe, context={'request': request}
            )
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        elif request.method == "DELETE":
            if not ShoppingСart.objects.filter(user=request.user,
                                               recipe=recipe).exists():
                raise exceptions.ValidationError(
                    'Рецепта нет в списке покупок.'
                )
            shopping_cart = get_object_or_404(
                ShoppingСart,
                user=request.user,
                recipe=recipe
            )
            shopping_cart.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=False, methods=['get'],
            url_path='download_shopping_cart',
            url_name='download_shopping_cart',
            permission_classes=[IsAuthenticated])
    def download_shopping_cart(self, request):
        shopping_list = RecipeIngredient.objects.filter(
            recipe__shopping_cart__user=request.user  # связь через модель ShoppingCart
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
        response['Content-Disposition'] = ('attachment; filename="shopping_list.txt"')
        return response

    @action(detail=True, methods=['post', 'delete'], url_path='favorite')
    def favorite(self, request, pk=None):
        recipe = get_object_or_404(Recipe, pk=pk)

        if request.method == 'POST':
            if Favorite.objects.filter(user=request.user, recipe=recipe).exists():
                raise exceptions.ValidationError('Рецепт уже добавлен в избранное.')
            Favorite.objects.create(user=request.user, recipe=recipe)

            # Принудительное обновление данных рецепта после добавления в избранное
            recipe.refresh_from_db()
            serializer = FavoriteSerializer(recipe, context={'request': request})
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        elif request.method == 'DELETE':
            favorite = Favorite.objects.filter(user=request.user, recipe=recipe)
            if not favorite.exists():
                raise exceptions.ValidationError('Рецепта нет в избранном.')
            favorite.delete()

            recipe.refresh_from_db()
            return Response(status=status.HTTP_204_NO_CONTENT)

















