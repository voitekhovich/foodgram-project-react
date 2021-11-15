from django_filters import rest_framework as filters

from app.models import Ingredient, Recipe, Tag


class CharInFilter(filters.MultipleChoiceFilter, filters.CharFilter):
    pass


class RecipeFilter(filters.FilterSet):
    is_favorited = filters.BooleanFilter(method='is_favorited_filter')
    is_in_shopping_cart = filters.BooleanFilter(
        method='is_in_shopping_cart_filter')
    author = filters.NumberFilter(field_name='author__id',)
    tags = filters.ModelMultipleChoiceFilter(
        field_name='tags__slug',
        to_field_name='slug',
        queryset=Tag.objects.all(),)

    class Meta:
        model = Recipe
        fields = ('is_favorited', 'is_in_shopping_cart', 'author', 'tags',)

    def is_favorited_filter(self, queryset, name, value):
        user = self.request.user
        if value and not user.is_anonymous:
            return queryset.filter(**{'favorites__user': user})
        return queryset

    def is_in_shopping_cart_filter(self, queryset, name, value):
        user = self.request.user
        if value and not user.is_anonymous:
            return queryset.filter(**{'shopping_carts__user': user})
        return Ingredient.objects.filter


class IngredientFilter(filters.FilterSet):
    name = filters.CharFilter(field_name='name', method='name_lower')

    class Meta:
        model = Ingredient
        fields = ('name',)

    def name_lower(self, queryset, name, value):
        return queryset.filter(name__istartswith=value.lower())
