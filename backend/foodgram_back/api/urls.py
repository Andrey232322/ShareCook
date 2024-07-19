from django.urls import include, path
from rest_framework.routers import DefaultRouter
#from .views import IngredientViewSet, RecipeViewSet, TagViewSet
from user.views import UserMEViewSet

app_name = 'api'

v1_router = DefaultRouter()

#v1_router.register('tags', TagViewSet)
#v1_router.register('ingredients', IngredientViewSet)
#v1_router.register('recipes', RecipeViewSet)
v1_router.register('users', UserMEViewSet)

urlpatterns = [
    path('api/', include(v1_router.urls)),
    # path('auth/', include('djoser.urls')),
    # path('auth/', include('djoser.urls.authtoken')),
]