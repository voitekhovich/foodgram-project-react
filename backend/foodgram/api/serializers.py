from app.models import (
    Favorite, Recipe, RecipeIngredients, Shopping_cart, Tag, Ingredient,
    UserSubscribe)
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator
from django.contrib.auth import get_user_model
from django.core.files.base import ContentFile
import base64

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('email', 'id', 'username', 'first_name', 'last_name',
                  'is_subscribed')

    def get_is_subscribed(self, obj):
        user = self.context.get('request').user
        if user.is_anonymous:
            return False
        return UserSubscribe.objects.filter(user=user, author=obj).exists()


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ('id', 'name', 'color', 'slug')


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = ('id', 'name', 'measurement_unit')


class RecipeIngredientsSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField(source='ingredient.id')
    name = serializers.ReadOnlyField(source='ingredient.name')
    measurement_unit = serializers.ReadOnlyField(
        source='ingredient.measurement_unit')

    class Meta:
        model = RecipeIngredients
        fields = ('id', 'name', 'measurement_unit', 'amount')


class ImageBase64Serializer(serializers.BaseSerializer):
    def to_representation(self, value):
        return value

    def to_internal_value(self, data):
        if not data:
            raise serializers.ValidationError({
                'image': 'Это поле обязательно к заполнению.'
            })

        format, imgstr = data.split(';base64,')
        ext = format.split('/')[-1]

        return ContentFile(base64.b64decode(imgstr), name='image.' + ext)


class RecipeSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True)
    author = UserSerializer(read_only=True)
    ingredients = RecipeIngredientsSerializer(
        source='recipeingredients_set', many=True)
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()
    image = ImageBase64Serializer()

    class Meta:
        model = Recipe
        fields = ('id', 'tags', 'author', 'ingredients', 'is_favorited',
                  'is_in_shopping_cart', 'name', 'image', 'text',
                  'cooking_time')

    def get_is_favorited(self, obj):
        user = self.context.get('request').user
        if user.is_anonymous:
            return False
        return Favorite.objects.filter(user=user, recipe=obj).exists()

    def get_is_in_shopping_cart(self, obj):
        user = self.context.get('request').user
        if user.is_anonymous:
            return False
        return Shopping_cart.objects.filter(user=user, recipe=obj).exists()


class RecipeShoppingCartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time')

        validators = [
            UniqueTogetherValidator(
                queryset=Shopping_cart.objects.all(),
                fields=('recipe', 'user')
            )
        ]
