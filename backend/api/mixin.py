from django.shortcuts import get_object_or_404
from recipes.models import Recipe
from rest_framework import status
from rest_framework.response import Response


class AddToRelationMixin:
    related_model = None
    serializer_class = None

    def add_and_delete_to_relation(self, request, pk, model,
                                   serializer_class, error_message):
        recipe = get_object_or_404(Recipe, pk=pk)
        relation_model = model.objects.filter(user=request.user, recipe=recipe)
        relation_model_exists = relation_model.exists()
        if request.method == 'POST':
            if relation_model_exists:
                return Response(
                    {'detail': error_message},
                    status=status.HTTP_400_BAD_REQUEST
                )

            model.objects.create(user=request.user, recipe=recipe)
            serializer = serializer_class(recipe, context={'request': request})
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        elif request.method == 'DELETE':
            if not relation_model_exists:
                return Response(
                    {'detail': f'Рецепта нет в {error_message}'},
                    status=status.HTTP_400_BAD_REQUEST
                )

            relation_model.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

        return None
