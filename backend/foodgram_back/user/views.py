
from djoser.views import UserViewSet
from rest_framework import generics, status,  viewsets
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from .models import User
from .serializers import UserSerializer, UserAvatarSerializer, PasswordSerializer
from rest_framework.exceptions import ValidationError
from rest_framework.decorators import action
from rest_framework.response import Response

class UserMEViewSet(viewsets.ModelViewSet):

    queryset = User.objects.all()
    serializer_class = UserSerializer

    @action(detail=False, methods=['get', 'put', 'patch'], url_path='me')
    def me(self, request):
        user = request.user
        if request.method in ['PUT', 'PATCH']:
            serializer = self.get_serializer(user, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)
        serializer = self.get_serializer(user)
        return Response(serializer.data)

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