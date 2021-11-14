from django.db import models
from django.db.models.constraints import UniqueConstraint
from django.contrib.auth import get_user_model
from pytils.translit import slugify

User = get_user_model()
User._meta.get_field('email')._unique = True


class Tag(models.Model):
    """Теги"""
    name = models.CharField('Название тега', unique=True, max_length=200)
    color = models.CharField('Цвет в HEX', max_length=7)
    slug = models.SlugField(
        'Уникальный слаг', max_length=200, unique=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)[:200]
        super().save(*args, **kwargs)


class Ingredient(models.Model):
    """Ингридиенты"""
    name = models.CharField('Название', unique=True, max_length=200)
    measurement_unit = models.CharField('Единицы измерения', max_length=200)

    def __str__(self):
        return f'{self.name}, {self.measurement_unit}'

    class Meta:
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'


class Recipe(models.Model):
    """Рецепты"""
    author = models.ForeignKey(
        User, related_name='recipes', on_delete=models.CASCADE,
        verbose_name='Автор рецепта',)
    name = models.CharField('Название рецепта', max_length=200,)
    image = models.ImageField('Ссылка на картинку', upload_to='image/',
                              blank=True, null=True,)
    text = models.TextField('Описание')
    cooking_time = models.IntegerField('Время приготовления (мин)')
    pub_date = models.DateTimeField('Дата публикации', auto_now_add=True)
    ingredients = models.ManyToManyField(
        Ingredient, through='RecipeIngredients', verbose_name='Ингредиенты',)
    tags = models.ManyToManyField(Tag, verbose_name='Теги',)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'
        ordering = ('-pub_date',)


class RecipeIngredients(models.Model):
    """Ингредиенты рецептов"""
    ingredient = models.ForeignKey(
        Ingredient, on_delete=models.CASCADE, verbose_name='Ингредиент')
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE,)
    amount = models.IntegerField('Количество',)

    def __str__(self):
        return f'{self.recipe} - {self.ingredient} - {self.amount}'

    class Meta:
        verbose_name = 'Ингредиенты рецептов'
        verbose_name_plural = 'Ингредиенты рецептов'
        UniqueConstraint(
            fields=('ingredient', 'recipe'),
            name='unique_ingredient_recipe'
        )


class Shopping_cart(models.Model):
    """Список покупок"""
    recipe = models.ForeignKey(
        Recipe, related_name='shopping_carts', on_delete=models.CASCADE,
        verbose_name='Рецепт',)
    user = models.ForeignKey(
        User, related_name='shopping_carts', on_delete=models.CASCADE,
        verbose_name='Пользователь',)

    def __str__(self):
        return f'{self.user.username} - {self.recipe}'

    class Meta:
        verbose_name = 'Список покупок'
        verbose_name_plural = 'Список покупок'
        UniqueConstraint(
            fields=('recipe', 'user'),
            name='unique_recipe_user'
        )


class Favorite(models.Model):
    """Избранные рецепты"""
    user = models.ForeignKey(
        User, related_name='favorites', on_delete=models.CASCADE,
        verbose_name='Пользователь',)
    recipe = models.ForeignKey(
        Recipe, related_name='favorites', on_delete=models.CASCADE,
        verbose_name='Рецепт',)

    def __str__(self):
        return f'{self.user.username} - {self.recipe}'

    class Meta:
        verbose_name = 'Избранные рецепты'
        verbose_name_plural = 'Избранные рецепты'
        UniqueConstraint(
            fields=('user', 'recipe'),
            name='unique_user_recipe'
        )


class UserSubscribe(models.Model):
    """Подписка на пользователя"""
    user = models.ForeignKey(
        User, related_name='followers', on_delete=models.CASCADE,
        verbose_name='Подписчик')
    author = models.ForeignKey(
        User, related_name='following', on_delete=models.CASCADE,
        verbose_name='Подписки')

    def __str__(self):
        return f'{self.user.username} - {self.author.username}'

    class Meta:
        verbose_name = 'Подписка на пользователя'
        verbose_name_plural = 'Подписка на пользователя'
        UniqueConstraint(
            fields=('user', 'author'),
            name='unique_user_author'
        )
