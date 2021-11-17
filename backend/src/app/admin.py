from django.contrib import admin

from .models import (Favorite, Ingredient, Recipe, RecipeIngredients,
                     ShoppingCart, Tag, UserSubscribe)


class RecipeIngredientsInline(admin.TabularInline):
    model = RecipeIngredients
    extra = 1


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'author',)
    list_display_links = ('name',)
    list_filter = ('tags',)
    inlines = (RecipeIngredientsInline,)
    readonly_fields = ('favorit_count',)
    search_fields = ('author__username', 'author__email', 'name')

    @admin.display(description='Добавлений в избранное')
    def favorit_count(self, instance):
        return Favorite.objects.filter(recipe=instance).count()


@admin.register(RecipeIngredients)
class RecipeIngredientsAdmin(admin.ModelAdmin):
    list_display = ('id', 'ingredient', 'recipe', 'amount',)
    search_fields = ('ingredient__name', 'recipe__name',)


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'color', 'slug')
    list_display_links = ('name',)
    search_fields = ('name',)


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'measurement_unit',)
    list_display_links = ('name',)
    search_fields = ('name',)


@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'recipe',)
    search_fields = ('user__username', 'user__email', 'recipe__name',)


@admin.register(ShoppingCart)
class ShoppingCartAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'recipe',)
    search_fields = ('user__username', 'user__email', 'recipe__name',)


@admin.register(UserSubscribe)
class UserSubscribeAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'author')
    search_fields = ('user__username', 'user__email', 'author__email')
