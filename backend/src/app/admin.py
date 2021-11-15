from django.contrib import admin

from .models import (Favorite, Ingredient, Recipe, RecipeIngredients,
                     Shopping_cart, Tag, UserSubscribe)


class RecipeIngredientsInline(admin.TabularInline):
    model = RecipeIngredients
    extra = 1


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ('name', 'author',)
    list_display_links = ('name',)
    list_filter = ('author', 'name', 'tags')
    inlines = (RecipeIngredientsInline,)
    readonly_fields = ('favorit_count',)

    @admin.display(description='Добавлений в избранное')
    def favorit_count(self, instance):
        return Favorite.objects.filter(recipe=instance).count()


@admin.register(RecipeIngredients)
class RecipeIngredientsAdmin(admin.ModelAdmin):
    list_display = ('ingredient', 'recipe', 'amount',)


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'color', 'slug')
    list_display_links = ('name',)
    search_fields = ('name',)


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ('name', 'measurement_unit',)
    list_filter = ('name',)


@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'recipe',)
    list_filter = ('user__username', 'recipe__name',)
    search_fields = ('user__username', 'recipe__name',)


@admin.register(Shopping_cart)
class Shopping_cartAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'recipe',)
    list_filter = ('user__username', 'recipe__name',)
    search_fields = ('user__username', 'recipe__name',)


@admin.register(UserSubscribe)
class UserSubscribeAdmin(admin.ModelAdmin):
    list_display = ('user', 'author')
