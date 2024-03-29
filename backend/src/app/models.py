from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.db.models.constraints import UniqueConstraint
from pytils.translit import slugify

from foodgram.settings import MAX_VALUE, MIN_VALUE

User = get_user_model()
User._meta.get_field('email')._unique = True


class Tag(models.Model):
    """Теги"""
    name = models.CharField('Название тега', unique=True, max_length=200)
    color = models.CharField('Цвет в HEX', max_length=7)
    slug = models.SlugField(
        'Уникальный слаг', max_length=200, unique=True, blank=True)

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)[:200]
        super().save(*args, **kwargs)


class Ingredient(models.Model):
    """Ингридиенты"""
    name = models.CharField('Название', unique=True, max_length=200)
    measurement_unit = models.CharField('Единицы измерения', max_length=200)

    class Meta:
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'

    def __str__(self):
        return f'{self.name}, {self.measurement_unit}'


class Recipe(models.Model):
    """Рецепты"""
    author = models.ForeignKey(
        User, related_name='recipes', on_delete=models.CASCADE,
        verbose_name='Автор рецепта',)
    name = models.CharField('Название рецепта', max_length=200,)
    image = models.ImageField('Ссылка на картинку', upload_to='image/',)
    text = models.TextField('Описание')
    cooking_time = models.IntegerField(
        'Время приготовления (мин)',
        validators=[
            MaxValueValidator(MAX_VALUE),
            MinValueValidator(MIN_VALUE)
        ])
    pub_date = models.DateTimeField('Дата публикации', auto_now_add=True)
    ingredients = models.ManyToManyField(
        Ingredient, through='RecipeIngredients', verbose_name='Ингредиенты',)
    tags = models.ManyToManyField(Tag, verbose_name='Теги',)

    class Meta:
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'
        ordering = ('-pub_date',)

    def __str__(self):
        return self.name


class RecipeIngredients(models.Model):
    """Ингредиенты рецептов"""
    ingredient = models.ForeignKey(
        Ingredient, on_delete=models.CASCADE, verbose_name='Ингредиент')
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE,)
    amount = models.IntegerField(
        'Количество',
        validators=[
            MaxValueValidator(MAX_VALUE),
            MinValueValidator(MIN_VALUE)
        ])

    class Meta:
        verbose_name = 'Ингредиенты рецептов'
        verbose_name_plural = 'Ингредиенты рецептов'
        constraints = (
            UniqueConstraint(
                fields=('ingredient', 'recipe'),
                name='unique_ingredient_recipe'
            ),
        )

    def __str__(self):
        return f'{self.recipe} - {self.ingredient} - {self.amount}'


class ShoppingCart(models.Model):
    """Список покупок"""
    recipe = models.ForeignKey(
        Recipe, related_name='shopping_carts', on_delete=models.CASCADE,
        verbose_name='Рецепт',)
    user = models.ForeignKey(
        User, related_name='shopping_carts', on_delete=models.CASCADE,
        verbose_name='Пользователь',)

    class Meta:
        verbose_name = 'Список покупок'
        verbose_name_plural = 'Список покупок'
        constraints = (
            UniqueConstraint(
                fields=('recipe', 'user'),
                name='unique_recipe_user'
            ),
        )

    def __str__(self):
        return f'{self.user.username} - {self.recipe}'


class Favorite(models.Model):
    """Избранные рецепты"""
    user = models.ForeignKey(
        User, related_name='favorites', on_delete=models.CASCADE,
        verbose_name='Пользователь',)
    recipe = models.ForeignKey(
        Recipe, related_name='favorites', on_delete=models.CASCADE,
        verbose_name='Рецепт',)

    class Meta:
        verbose_name = 'Избранные рецепты'
        verbose_name_plural = 'Избранные рецепты'
        constraints = (
            UniqueConstraint(
                fields=('user', 'recipe'),
                name='unique_user_recipe'
            ),
        )

    def __str__(self):
        return f'{self.user.username} - {self.recipe}'


class UserSubscribe(models.Model):
    """Подписка на пользователя"""
    user = models.ForeignKey(
        User, related_name='followers', on_delete=models.CASCADE,
        verbose_name='Подписчик')
    author = models.ForeignKey(
        User, related_name='following', on_delete=models.CASCADE,
        verbose_name='Подписки')

    class Meta:
        verbose_name = 'Подписка на пользователя'
        verbose_name_plural = 'Подписка на пользователя'
        constraints = (
            UniqueConstraint(
                fields=('user', 'author'),
                name='unique_user_author'
            ),
        )

    def __str__(self):
        return f'{self.user.username} - {self.author.username}'
