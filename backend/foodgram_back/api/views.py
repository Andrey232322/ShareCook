# from rest_framework import status, viewsets
#
# from resept.models import Tag, Ingredient, Recipes
# from .serializers import TagSerializer, IngredientSerializer, RecipesSerializer
#
# class TagViewSet(viewsets.ReadOnlyModelViewSet):
#     """Вьюсет тега."""
#     queryset = Tag.objects.all()
#     serializer_class = TagSerializer
#     #permission_classes = [IsAuthenticatedOrReadOnly]
#     pagination_class = None
#
#
# class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
#     """Вьюсет ингридиента."""
#     queryset = Ingredient.objects.all()
#     #permission_classes = [IsAuthenticatedOrReadOnly]
#     serializer_class = IngredientSerializer
#     #filter_backends = [IngredientSearchFilter]
#     search_fields = ('^name',)
#     pagination_class = None
#
# class RecipeViewSet(viewsets.ReadOnlyModelViewSet):
#     queryset = Recipes.objects.all()
#     serializer_class = RecipesSerializer