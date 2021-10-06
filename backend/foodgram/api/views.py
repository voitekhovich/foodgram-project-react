from rest_framework.generics import get_object_or_404
from app.models import Ingredient, Recipe, Shopping_cart, Tag, Favorite
from .filters import RecipeFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import serializers, viewsets, status
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from .serializers import (RecipeSerializer, RecipeShoppingCartSerializer,
                          TagSerializer, IngredientSerializer)


class SetLimitPagination(PageNumberPagination):
    page_size = 6
    page_size_query_param = 'limit'
    max_page_size = 100


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    pagination_class = SetLimitPagination
    filter_backends = (DjangoFilterBackend,)
    filterset_class = RecipeFilter

    def get_serializer_class(self):
        if self.action in ('shopping_cart', 'favorite'):
            return RecipeShoppingCartSerializer
        return RecipeSerializer

    @action(detail=False)
    def download_shopping_cart(self, request):
        """ ТУТ БУДЕМ ОТДАВАТЬ СПИСОК ПОКУПОК """
        serializer = self.get_serializer()
        return Response(serializer.data)

    @action(detail=True, methods=('get', 'delete'))
    def shopping_cart(self, request, pk=None):
        """Добавить/удалить рецепт в список покупок."""

        recipe = get_object_or_404(Recipe, id=pk)
        user = request.user

        if request.method == 'DELETE':
            Shopping_cart.objects.filter(recipe=pk, user=user).delete()
            return Response(status.HTTP_204_NO_CONTENT)

        if Shopping_cart.objects.filter(recipe=recipe, user=user).exists():
            raise serializers.ValidationError('Рецепт уже в списке покупок')

        Shopping_cart.objects.create(recipe=recipe, user=user)
        serializer = self.get_serializer(recipe)
        return Response(serializer.data)

    @action(detail=True, methods=('get', 'delete'))
    def favorite(self, request, pk=None):
        """Добавить/удалить рецепт в избранное."""

        recipe = get_object_or_404(Recipe, id=pk)
        user = request.user

        if request.method == 'DELETE':
            Favorite.objects.filter(recipe=pk, user=user).delete()
            return Response(status.HTTP_204_NO_CONTENT)

        if Favorite.objects.filter(recipe=recipe, user=user).exists():
            raise serializers.ValidationError('Рецепт уже в избранном')

        Favorite.objects.create(recipe=recipe, user=user)
        serializer = self.get_serializer(recipe)
        return Response(serializer.data)


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
