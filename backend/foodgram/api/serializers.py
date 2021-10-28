from app.models import (
    Favorite, Recipe, RecipeIngredients, Shopping_cart, Tag, Ingredient,
    UserSubscribe)

import base64

from django.contrib.auth import get_user_model
from django.core.files.base import ContentFile

from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

User = get_user_model()


"""Пользователи"""


class SpecialUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'email', 'id', 'username', 'first_name', 'last_name', 'password')
        extra_kwargs = {
            'email': {'required': True},
            'username': {'required': True},
            'first_name': {'required': True},
            'last_name': {'required': True},
            'password': {'required': True, 'write_only': True},
        }

    def create(self, validated_data):
        user = User(
            email=validated_data['email'],
            username=validated_data['username'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
        )
        user.set_password(validated_data['password'])
        user.save()
        return user


class SubscribeUserSerializer(serializers.ModelSerializer):
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


class SubscriptionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('author__email', 'author__id', 'author__username',
                  'author__first_name', 'author__last_name',)


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


"""Рецепты"""


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


class RecipeSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True, read_only=True)
    author = UserSerializer(read_only=True)
    ingredients = RecipeIngredientsSerializer(
        source='recipeingredients_set', many=True)
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()

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


"""Создание рецепта"""


class ImgBase64Serializer(serializers.Field):
    def to_representation(self, value):
        return value.url

    def to_internal_value(self, data):
        if not data:
            raise serializers.ValidationError({
                'image': 'Это поле обязательно к заполнению.'
            })

        format, imgstr = data.split(';base64,')
        ext = format.split('/')[-1]

        return ContentFile(base64.b64decode(imgstr), name='image.' + ext)


class RecipeIngredientSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()

    class Meta:
        model = RecipeIngredients
        fields = ('id', 'amount')


class RecipeCreateSerializer(serializers.ModelSerializer):
    author = serializers.HiddenField(default=serializers.CurrentUserDefault())
    ingredients = RecipeIngredientSerializer(many=True)
    image = ImgBase64Serializer()

    class Meta:
        model = Recipe
        fields = (
            'author', 'ingredients', 'tags', 'image', 'name', 'text',
            'cooking_time')

    def to_representation(self, instance):
        serializer = RecipeSerializer(
            instance, context={'request': self.context['request']})
        return serializer.data

    def set_recipe_ingredients(self, ingredients, instance):
        for ingredient in ingredients:
            current_ingredient = Ingredient.objects.get(
                pk=ingredient['id'])
            RecipeIngredients.objects.create(
                recipe=instance, ingredient=current_ingredient,
                amount=ingredient['amount'],
            )

    def create(self, validated_data):

        ingredients = validated_data.pop('ingredients')
        tags = validated_data.pop('tags')

        recipe = Recipe.objects.create(**validated_data)
        recipe.tags.set(tags)

        self.set_recipe_ingredients(ingredients, recipe)

        return recipe

    def update(self, instance, validated_data):

        ingredients = validated_data.pop('ingredients')
        tags = validated_data.pop('tags')

        instance.tags.set(tags)
        for key, value in validated_data.items():
            setattr(instance, key, value)

        RecipeIngredients.objects.filter(recipe=instance).delete()
        self.set_recipe_ingredients(ingredients, instance)

        instance.save()

        return instance


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
