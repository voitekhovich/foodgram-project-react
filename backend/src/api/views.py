from django.contrib.auth import get_user_model
from django.db.models import Sum
from django.http import FileResponse
from django_filters.rest_framework import DjangoFilterBackend
from djoser.views import UserViewSet
from rest_framework import permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

from app.models import (Favorite, Ingredient, Recipe, RecipeIngredients,
                        Shopping_cart, Tag, UserSubscribe)
from foodgram.settings import (MAX_PAGE_SIZE, PAGE_SIZE, PAGE_SIZE_QUERY_PARAM,
                               PDF_FILE_NAME)

from .constants import Actions, HTTPMethods
from .filters import IngredientFilter, RecipeFilter
from .permissions import IsOwnerOrReadOnly
from .serializers import (IngredientSerializer, RecipeCreateSerializer,
                          RecipeSerializer, RecipeShoppingCartSerializer,
                          SubscriptionsSerializer, TagSerializer)
from .services import create_pdf

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
        if self.action == Actions.SUBSCRIPTIONS:
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

    @action(detail=True, methods=(HTTPMethods.GET, HTTPMethods.DELETE))
    def subscribe(self, request, id=None):
        """Подписаться/отписаться на автора."""

        author = get_object_or_404(User, id=id)
        user = request.user

        if request.method == 'DELETE':
            UserSubscribe.objects.filter(author=author, user=user).delete()
            return Response(status.HTTP_204_NO_CONTENT)

        UserSubscribe.objects.get_or_create(author=author, user=user)
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
        if self.action in (Actions.SHOPPING_CART, Actions.FAVORITE):
            return RecipeShoppingCartSerializer
        if self.action in (
                Actions.CREATE, Actions.UPDATE, Actions.PARTIAL_UPDATE):
            return RecipeCreateSerializer
        return RecipeSerializer

    @action(detail=False)
    def download_shopping_cart(self, request):
        """Отправить PDF список."""
        user = request.user
        recipes = Shopping_cart.objects.filter(user=user).values('recipe')
        shop_list = (
            RecipeIngredients.objects.filter(recipe__in=recipes)
            .values('ingredient__name', 'ingredient__measurement_unit')
            .annotate(Sum('amount'))
        )
        buffer = create_pdf(shop_list)
        return FileResponse(
            buffer, as_attachment=True, filename=PDF_FILE_NAME)

    @action(detail=True, methods=(HTTPMethods.GET, HTTPMethods.DELETE))
    def shopping_cart(self, request, pk=None):
        """Добавить/удалить рецепт в список покупок."""

        recipe = get_object_or_404(Recipe, id=pk)
        user = request.user

        if request.method == 'DELETE':
            Shopping_cart.objects.filter(recipe=pk, user=user).delete()
            return Response(status.HTTP_204_NO_CONTENT)

        Shopping_cart.objects.get_or_create(recipe=recipe, user=user)
        serializer = self.get_serializer(recipe)
        return Response(serializer.data)

    @action(detail=True, methods=(HTTPMethods.GET, HTTPMethods.DELETE))
    def favorite(self, request, pk=None):
        """Добавить/удалить рецепт в избранное."""

        recipe = get_object_or_404(Recipe, id=pk)
        user = request.user

        if request.method == 'DELETE':
            Favorite.objects.filter(recipe=pk, user=user).delete()
            return Response(status.HTTP_204_NO_CONTENT)

        Favorite.objects.get_or_create(recipe=recipe, user=user)
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
