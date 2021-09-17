from django.db import models
from django.contrib.auth import get_user_model
from pytils.translit import slugify

User = get_user_model()


class Recipe(models.Model):
    author = models.ForeignKey(User, related_name='recipes',
                               on_delete=models.CASCADE,
                               verbose_name='Автор рецепта')
    name = models.CharField(max_length=200, verbose_name='Название')
    image = models.ImageField(verbose_name='Ссылка на картинку на сайте')
    text = models.TextField(verbose_name='Описание')
    cooking_time = models.IntegerField(
        verbose_name='Время приготовления (мин)')
    pub_date = models.DateTimeField(verbose_name='Дата публикации',
                                    auto_now_add=True)


class Tag(models.Model):
    name = models.CharField(verbose_name='Название', max_length=200)
    color = models.CharField(verbose_name='Цвет в HEX', max_length=7)
    slug = models.CharField(verbose_name='Уникальный слаг', max_length=200,
                            unique=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)[:200]
        super().save(*args, **kwargs)


class Tags(models.Model):
    tag = models.ForeignKey(Tag, related_name='recipes',
                            on_delete=models.CASCADE,
                            verbose_name='Список рецептов')
    recipe = models.ForeignKey(Recipe, related_name='tags',
                               on_delete=models.CASCADE,
                               verbose_name='Список тегов')


class Ingredient(models.Model):
    name = models.CharField(verbose_name='Название', max_length=200)
    measurement_unit = models.CharField(verbose_name='Единицы измерения',
                                        max_length=200)


class Ingredients(models.Model):
    ingredient = models.ForeignKey(Ingredient, related_name='recipes',
                                   on_delete=models.CASCADE,
                                   verbose_name='Список рецептов')
    recipe = models.ForeignKey(Recipe, related_name='ingredients',
                               on_delete=models.CASCADE,
                               verbose_name='Список ингредиентов')
    amount = models.IntegerField(verbose_name='Количество')


class Shopping_cart(models.Model):
    recipe = models.ForeignKey(Recipe, related_name='shopping_carts',
                               on_delete=models.CASCADE,
                               verbose_name='Список покупок')
    user = models.ForeignKey(User, related_name='shopping_carts',
                             on_delete=models.CASCADE,
                             verbose_name='Список покупок')


class Favorite(models.Model):
    user = models.ForeignKey(User, related_name='favorites',
                             on_delete=models.CASCADE,
                             verbose_name='Избранные')
    recipe = models.ForeignKey(Recipe, related_name='favorites',
                               on_delete=models.CASCADE,
                               verbose_name='Избранные')
