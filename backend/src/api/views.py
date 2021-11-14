from app.models import (
    Ingredient, Recipe, RecipeIngredients, Shopping_cart, Tag, Favorite,
    UserSubscribe)

from foodgram.settings import (
    PAGE_SIZE, MAX_PAGE_SIZE, PAGE_SIZE_QUERY_PARAM, PDF_FILE_NAME)

from .permissions import IsOwnerOrReadOnly
from .filters import RecipeFilter, IngredientFilter
from .serializers import (
    RecipeCreateSerializer, RecipeSerializer, SubscriptionsSerializer,
    TagSerializer,
    RecipeShoppingCartSerializer,
    IngredientSerializer)
from .services import create_pdf

from rest_framework.generics import get_object_or_404

from django.contrib.auth import get_user_model
from django.db.models import Sum
from django_filters.rest_framework import DjangoFilterBackend

from rest_framework import serializers, permissions, viewsets, status
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.generics import get_object_or_404

from djoser.views import UserViewSet

User = get_user_model()


class SetLimitPagination(PageNumberPagination):
    page_size = PAGE_SIZE
    page_size_query_param = PAGE_SIZE_QUERY_PARAM
    max_page_size = MAX_PAGE_SIZE


"""Пользователи"""


class CustomUserViewSet(UserViewSet):
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,
                          IsOwnerOrReadOnly)
    pagination_class = SetLimitPagination

    def get_serializer_class(self):
        if self.action == 'subscriptions':
            return SubscriptionsSerializer
        return super().get_serializer_class()

    @action(detail=False)
    def subscriptions(self, request):
        """Список авторов, на которых подписан пользователь"""
        user = request.user
        authors = User.objects.filter(following__user=user)

        page = self.paginate_queryset(authors)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(authors, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=('get', 'delete'))
    def subscribe(self, request, id=None):
        """Подписаться/отписаться на автора."""

        author = get_object_or_404(User, id=id)
        user = request.user

        if request.method == 'DELETE':
            UserSubscribe.objects.filter(author=author, user=user).delete()
            return Response(status.HTTP_204_NO_CONTENT)

        if UserSubscribe.objects.filter(author=author, user=user).exists():
            raise serializers.ValidationError(
                'Вы уже подписаны на этого автора')

        UserSubscribe.objects.create(author=author, user=user)
        serializer = self.get_serializer(author)
        return Response(serializer.data)


"""Рецепты"""


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    pagination_class = SetLimitPagination
    permission_classes = (
        permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly,)
    filter_backends = (DjangoFilterBackend,)
    filterset_class = RecipeFilter

    def get_serializer_class(self):
        if self.action in ('shopping_cart', 'favorite'):
            return RecipeShoppingCartSerializer
        if self.action in ('create', 'update', 'partial_update'):
            return RecipeCreateSerializer
        return RecipeSerializer

    @action(detail=False)
    def download_shopping_cart(self, request):
        """Отправить PDF список."""
        from django.http import FileResponse
        user = request.user
        recipes = Shopping_cart.objects.filter(user=user).values('recipe')
        shop_list = RecipeIngredients.objects.filter(recipe__in=recipes)\
            .values('ingredient__name', 'ingredient__measurement_unit')\
            .annotate(Sum('amount')).order_by()
        buffer = create_pdf(shop_list)
        return FileResponse(
            buffer, as_attachment=True, filename=PDF_FILE_NAME)

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
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    filter_backends = (DjangoFilterBackend,)
    filterset_class = IngredientFilter
