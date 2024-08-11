import base64
import mimetypes

from django.contrib.auth import get_user_model
from django.core.files.storage import default_storage
from django.db.models import Sum
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from recipes.models import (FavoritesList, Ingredient, Recipe,
                            RecipeIngredient, ShoppingList, Tag)
from rest_framework import filters, status, viewsets
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import (AllowAny, IsAuthenticated,
                                        IsAuthenticatedOrReadOnly)
from rest_framework.response import Response
from users.models import Follow

from .filters import IngredientFilter, RecipeFilter
from .mixins import CreateListRetrieveViewSet
from .paginators import LimitPageNumberPaginator
from .serializers import (AvatarUpdateSerializer, FavoritesListSerializer,
                          IngredientSerializer, RecipeCreateSerializer,
                          RecipeGetSerializer, SetPasswordSerializer,
                          ShoppingCartSerializer, SubscribeSerializer,
                          SubscriptionSerializer, TagSerializer,
                          UserCreateSerializer, UserReadSerializer)

User = get_user_model()


class UserViewSet(CreateListRetrieveViewSet):
    queryset = User.objects.all()
    filter_backends = (DjangoFilterBackend, filters.SearchFilter)
    search_fields = ('username',)
    filterset_fields = ('username',)
    permission_classes = (AllowAny,)

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve'):
            return UserReadSerializer
        elif self.action == 'set_password':
            return SetPasswordSerializer
        elif self.action == 'subscribe':
            return SubscribeSerializer
        elif self.action == 'avatar':
            return AvatarUpdateSerializer
        elif self.action == 'me':
            return UserReadSerializer
        return UserCreateSerializer

    @action(
        methods=('get',),
        detail=False,
        permission_classes=(IsAuthenticated,),
    )
    def me(self, request):
        """Информация о своем аккаунте."""

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

    @action(
        methods=('post',),
        detail=False,
        serializer_class=SetPasswordSerializer,
        permission_classes=(IsAuthenticated,),
    )
    def set_password(self, request):
        """Страница смены пароля."""

        user = request.user
        serializer = self.get_serializer(user, data=request.data)
        serializer.is_valid(raise_exception=True)
        old_password = serializer.validated_data.get('current_password')
        new_password = serializer.validated_data.get('new_password')
        if not user.check_password(old_password):
            return Response(
                'Неверный пароль',
                status=status.HTTP_400_BAD_REQUEST
            )
        user.set_password(new_password)
        user.save()
        return Response('Пароль успешно изменен', status=status.HTTP_200_OK)

    @action(
        methods=('get',),
        detail=False,
        serializer_class=SubscriptionSerializer,
        permission_classes=(IsAuthenticated,),
        pagination_class=LimitPageNumberPaginator
    )
    def subscriptions(self, request):
        """Просмотр подписок пользователя."""

        user = request.user
        subscriptions = user.follower.all()
        users_id = subscriptions.values_list('author_id', flat=True)
        users = User.objects.filter(id__in=users_id)
        paginated_queryset = self.paginate_queryset(users)
        serializer = self.serializer_class(paginated_queryset,
                                           context={'request': request},
                                           many=True)
        return self.get_paginated_response(serializer.data)

    @action(detail=True,
            methods=('post', 'delete'),
            serializer_class=SubscribeSerializer,
            permission_classes=(IsAuthenticated,),
            )
    def subscribe(self, request, pk=None):
        """Добавление и удаление подписок пользователя."""

        if request.method == 'POST':
            serializer = self.get_serializer(
                data=request.data,
                context={'request': request, 'id': pk}
            )
            serializer.is_valid(raise_exception=True)
            response_data = serializer.save(id=pk)
            return Response(
                {'message': 'Подписка успешно создана',
                 'data': response_data},
                status=status.HTTP_201_CREATED
            )
        elif request.method == 'DELETE':
            subscription = get_object_or_404(
                Follow, user=self.request.user,
                author=get_object_or_404(User, pk=pk)
            )
            subscription.delete()
            return Response(
                {'Успешная отписка'},
                status=status.HTTP_204_NO_CONTENT
            )


class RecipeViewSet(viewsets.ModelViewSet):
    """Работа с рецептами."""

    queryset = Recipe.objects.all()
    permission_classes = (IsAuthenticatedOrReadOnly,)
    http_method_names = [
        'get',
        'post',
        'patch',
        'delete',
    ]
    filter_backends = (DjangoFilterBackend,)
    filterset_class = RecipeFilter
    pagination_class = LimitPageNumberPaginator

    def get_serializer_class(self):
        """Определение серилизатора."""

        if self.action in ('list', 'retrieve'):
            return RecipeGetSerializer
        elif self.action == 'favorite':
            return FavoritesListSerializer
        elif self.action == 'shopping_cart':
            return ShoppingCartSerializer
        return RecipeCreateSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def perform_update(self, serializer):
        serializer.save(author=self.request.user)

    @action(detail=True, methods=['get'],
            url_path='get-link',
            url_name='get-link')
    def get_link(self, request, pk=None):
        recipe = self.get_object()
        short_link = f"https://random-foodgram.zapto.org/s/{recipe.pk}d0"
        return Response({'short-link': short_link})

    @action(
        methods=('post', 'delete',),
        detail=True,
        serializer_class=FavoritesListSerializer,
        permission_classes=(IsAuthenticated,),
    )
    def favorite(self, request, pk=None):
        """Добавление/удаление рецептов из избранного."""

        if request.method == 'POST':
            serializer = self.get_serializer(
                data=request.data,
                context={'request': request, 'recipe_id': pk}
            )
            serializer.is_valid(raise_exception=True)
            response_data = serializer.save(id=pk)
            return Response(
                {'message': 'Рецепт успешно добавлен в избранное.',
                 'data': response_data},
                status=status.HTTP_201_CREATED
            )
        elif request.method == 'DELETE':
            get_object_or_404(
                FavoritesList, user=self.request.user,
                recipe=get_object_or_404(Recipe, pk=pk)).delete()
            return Response(
                {'Рецепт успешно удален из избранного'},
                status=status.HTTP_204_NO_CONTENT
            )

    @action(
        methods=('post', 'delete',),
        detail=True,
        serializer_class=ShoppingCartSerializer,
        permission_classes=(IsAuthenticated,),
    )
    def shopping_cart(self, request, pk=None):
        """Добавление/удаление рецепта из корзины."""

        if self.request.method == 'POST':
            return self.add_recipe_to_cart(request, pk)
        elif self.request.method == 'DELETE':
            return self.remove_recipe_from_cart(request, pk)

    def add_recipe_to_cart(self, request, pk):
        serializer = self.get_serializer(
            data=request.data,
            context={'request': request, 'recipe_id': pk}
        )
        serializer.is_valid(raise_exception=True)
        response_data = serializer.save(id=pk)
        return Response(
            {'message': 'Рецепт успешно добавлен в список покупок',
             'data': response_data},
            status=status.HTTP_201_CREATED
        )

    def remove_recipe_from_cart(self, request, pk):
        get_object_or_404(
            ShoppingList,
            user=self.request.user,
            recipe=get_object_or_404(Recipe, pk=pk)
        ).delete()
        return Response(
            {'message': 'Рецепт успешно удален из списка покупок'},
            status=status.HTTP_204_NO_CONTENT
        )

    @action(detail=False, methods=['get'],
            url_path='download_shopping_cart',
            url_name='download_shopping_cart',
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
        response['Content-Disposition'] = ('attachment; '
                                           'filename="shopping_list.txt"')
        return response


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    """Получение списка ингридиентов."""

    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    permission_classes = (AllowAny,)
    filter_backends = (DjangoFilterBackend,)
    filterset_class = IngredientFilter
    pagination_class = None


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    """Получение списка тэгов."""

    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = (AllowAny,)
    pagination_class = None
