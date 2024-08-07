from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import TagViewSet, IngredientViewSet, RecipeViewSet
from user.views import UserMEViewSet
from django.conf import settings
from django.conf.urls.static import static

app_name = 'api'

v1_router = DefaultRouter()

v1_router.register('tags', TagViewSet)
v1_router.register('ingredients.py', IngredientViewSet)
v1_router.register('users', UserMEViewSet)
v1_router.register(r'recipes', RecipeViewSet)

urlpatterns = [
    path('', include(v1_router.urls)),
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)