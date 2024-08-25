from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import RecipeViewSet, TagViewSet, IngredientViewSet

v_router = DefaultRouter()

v_router.register(r'recipes', RecipeViewSet, basename='recipes')
v_router.register('tags', TagViewSet)
v_router.register('ingredients', IngredientViewSet)

urlpatterns = [
    path('', include(v_router.urls)),
]