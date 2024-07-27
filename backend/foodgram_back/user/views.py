from rest_framework import mixins

from django.shortcuts import get_object_or_404
from djoser.views import UserViewSet
from rest_framework import generics, status, viewsets, exceptions
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import User, Subscription
from .serializers import UserSerializer, UserAvatarSerializer, PasswordSerializer, SubscriptionSerializer
from rest_framework.exceptions import ValidationError
from rest_framework.decorators import action
from rest_framework.response import Response
from api.permissions import IsAuthenOrReadOnly

#from .serializers import SubscriptionSerializer


class UserMEViewSet(viewsets.ModelViewSet):

    queryset = User.objects.all().order_by('id')
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)
    @action(detail=False, methods=['get'], url_path='me', permission_classes=(IsAuthenticated,))
    def me(self, request):
        serializer = self.get_serializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=['put', 'patch', 'delete'], url_path='me/avatar',
            serializer_class=UserAvatarSerializer)
    def avatar(self, request):
        user = request.user
        if request.method == 'DELETE':
            user.avatar.delete()
            user.avatar = None
            user.save()
            return Response(status=status.HTTP_204_NO_CONTENT)
        elif request.method in ['PUT', 'PATCH']:
            serializer = self.get_serializer(user, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        except ValidationError as e:
            # Get the required fields from the serializer
            required_fields = [field for field in serializer.fields if serializer.fields[field].required]
            error_response = {
                "detail": "Validation error",
                "errors": e.detail,
                "required_fields": required_fields
            }
            return Response(error_response, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['post'], url_path='set_password', serializer_class=PasswordSerializer)
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

    @action(detail=False, methods=['get'],
            serializer_class=SubscriptionSerializer,
            )


    @action(detail=False, methods=['get'], url_path='subscriptions', url_name='subscriptions')
    def subscriptions(self, request):
        user = self.request.user
        subscriptions = User.objects.filter(
            subscribing__user=user
        ).prefetch_related('recipes').order_by('id')

        paginated_queryset = self.paginate_queryset(subscriptions)
        if paginated_queryset is not None:
            serializer = self.get_serializer(paginated_queryset, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(subscriptions, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['post', 'delete'],
            serializer_class=SubscriptionSerializer)
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