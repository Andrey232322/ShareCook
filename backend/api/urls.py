from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import IngredientViewSet, RecipeViewSet, TagViewSet, UserViewSet


v_router = DefaultRouter()

v_router.register(r'recipes', RecipeViewSet, basename='recipes')
v_router.register('tags', TagViewSet)
v_router.register('ingredients', IngredientViewSet)
v_router.register('users', UserViewSet, basename='users')

urlpatterns = [
    path('', include(v_router.urls)),
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
]
