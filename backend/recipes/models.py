from colorfield.fields import ColorField
from django.contrib.auth import get_user_model
from django.core.validators import (MaxValueValidator, MinValueValidator,
                                    RegexValidator)
from django.db import models

import core.constants as const

User = get_user_model()


class Tag(models.Model):
    name = models.CharField(
        max_length=const.FIELD_LENGTH_200,
        verbose_name='Имя тэга'
    )
    color = ColorField(
        verbose_name='Цвет'
    )
    slug = models.SlugField(
        max_length=const.FIELD_LENGTH_200,
        unique=True,
        verbose_name='Слаг',
        validators=[
            RegexValidator(
                regex='^[-a-zA-Z0-9_]+$',
                message='В слаге использованы недопустимые символы.',
            ),
        ]
    )

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('slug',)
        verbose_name = 'Тэг'
        verbose_name_plural = 'Тэги'


class Ingredient(models.Model):
    name = models.CharField(
        max_length=const.FIELD_LENGTH_200,
        verbose_name='Ингредиент'
    )
    measurement_unit = models.CharField(
        max_length=const.FIELD_LENGTH_200,
        verbose_name='Единица измерения'
    )

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('name',)
        unique_together = ('name', 'measurement_unit',)
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'


class Content(models.Model):
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        related_name='contents',
        verbose_name='Ингредиент'
    )
    recipe = models.ForeignKey(
        'Recipe',
        on_delete=models.CASCADE,
        related_name='contents',
        verbose_name='Рецепт'
    )
    amount = models.PositiveSmallIntegerField(
        validators=(
            MinValueValidator(const.MIN_AMOUNT),
            MaxValueValidator(const.MAX_AMOUNT),
        ),
        verbose_name='Количество'
    )

    def __str__(self):
        return f'{self.ingredient} ({self.amount}) -> {self.recipe}'

    class Meta:
        ordering = ('recipe', 'ingredient',)
        unique_together = ('recipe', 'ingredient',)
        verbose_name = 'Состав'
        verbose_name_plural = 'Состав'


class UserRecipeRelation(models.Model):
    user = models.ForeignKey(
        User,
        related_name='%(class)ss',
        on_delete=models.CASCADE,
        verbose_name='Пользователь',
    )
    recipe = models.ForeignKey(
        'Recipe',
        related_name='%(class)ss',
        on_delete=models.CASCADE,
        verbose_name='Рецепт'
    )

    class Meta:
        abstract = True
        ordering = ('user', 'recipe',)
        unique_together = ('user', 'recipe',)

    @property
    def is_owner(self, user):
        return self.user == user


class Favorite(UserRecipeRelation):

    class Meta:
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'


class Shoppingcart(UserRecipeRelation):

    class Meta:
        verbose_name = 'Покупка'
        verbose_name_plural = 'Покупки'


class Recipe(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='recipes',
        verbose_name='Автор рецепта',
    )
    name = models.CharField(
        max_length=const.FIELD_LENGTH_200,
        verbose_name='Название рецепта'
    )
    text = models.CharField(
        max_length=const.FIELD_LENGTH_200,
        verbose_name='Описание рецепта'
    )
    tags = models.ManyToManyField(
        Tag,
        related_name='recipes',
        verbose_name='Список тегов'
    )
    ingredients = models.ManyToManyField(
        Ingredient,
        through=Content,
        related_name='recipes',
        verbose_name='Список ингредиентов'
    )
    image = models.ImageField(
        upload_to='recipes/images/',
        null=True,
        default=None,
        verbose_name='Изображение блюда'
    )
    pub_date = models.DateTimeField(
        auto_now_add=True,
        db_index=True,
        verbose_name='Дата публикации'
    )
    cooking_time = models.PositiveSmallIntegerField(
        validators=(
            MinValueValidator(const.MIN_AMOUNT),
            MaxValueValidator(const.MAX_AMOUNT),
        ),
        verbose_name='Время приготовления'
    )

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('pub_date', 'id')
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'

    @property
    def is_author(self, user):
        return self.author == user
