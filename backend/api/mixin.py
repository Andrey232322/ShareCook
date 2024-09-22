from django.shortcuts import get_object_or_404
from recipes.models import Recipe
from rest_framework import exceptions, status
from rest_framework.response import Response


class AddToRelationMixin:
    related_model = None  # Модель, с которой ведется работа
    serializer_class = None  # Сериализатор для ответа

    def add_to_relation(self, request, pk, model,
                        serializer_class, error_message):
        recipe = get_object_or_404(Recipe, pk=pk)

        if request.method == 'POST':
            if model.objects.filter(user=request.user, recipe=recipe).exists():
                raise exceptions.ValidationError(error_message)

            model.objects.create(user=request.user, recipe=recipe)
            serializer = serializer_class(recipe, context={'request': request})
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        elif request.method == 'DELETE':
            instance = model.objects.filter(user=request.user, recipe=recipe)
            if not instance.exists():
                raise exceptions.ValidationError(f'Рецепта '
                                                 f'нет в {error_message}')

            instance.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

        return None
