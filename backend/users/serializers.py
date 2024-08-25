# import base64
# import os
# import sys
#
# sys.path.append(os.path.join(os.getcwd(), '..'))
# from recipes.models import Recipe
# from api.serializers import RecipeSerializer
# from django.core.files.base import ContentFile
# from djoser.serializers import UserCreateSerializer, UserSerializer
# from rest_framework import serializers
#
# from .models import User
#
#
# class Base64ImageField(serializers.ImageField):
#     def to_internal_value(self, data):
#         if isinstance(data, str) and data.startswith('data:image'):
#             format, imgstr = data.split(';base64,')
#             ext = format.split('/')[-1]
#             data = ContentFile(base64.b64decode(imgstr), name='temp.' + ext)
#         return super().to_internal_value(data)
#
# class UserCreateSerializer(UserCreateSerializer):
#
#     class Meta:
#         model = User
#         fields = (
#             'email',
#             'username',
#             'first_name',
#             'last_name',
#             'password'
#         )
# class UserReadSerializer(UserSerializer):
#
#     class Meta:
#         model = User
#         fields = (
#             'email',
#             'id',
#             'username',
#             'first_name',
#             'last_name',
#             'is_subscribed',
#             'avatar'
#         )
#
# class AvatarUpdateSerializer(serializers.ModelSerializer):
#     avatar = Base64ImageField()
#
#     class Meta:
#         model = User
#         fields = ('avatar',)
#
# class PasswordSerializer(serializers.Serializer):
#     new_password = serializers.CharField(write_only=True, required=True)
#     current_password = serializers.CharField(write_only=True, required=True)
#
# class SubscriptionSerializer(UserSerializer):
#     recipes = serializers.SerializerMethodField(read_only=True)
#     recipes_count = serializers.SerializerMethodField()
#
#     class Meta:
#         model = User
#         fields = ("email", "id", "username", "first_name", "last_name",
#                   "is_subscribed", "recipes", "recipes_count")
#
#     def get_recipes(self, obj):
#         request = self.context.get('request')
#         limit = request.query_params.get('recipes_limit')
#         recipes = Recipe.objects.filter(author=obj)
#         if limit:
#             recipes = recipes[:int(limit)]
#         serializer = RecipeSerializer(recipes, many=True)
#         return serializer.data
#
#     def get_recipes_count(self, obj):
#         return Recipe.objects.filter(author=obj).count()