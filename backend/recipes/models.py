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
        blank=True,
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

    class Meta:
        verbose_name = 'Тэг'
        verbose_name_plural = 'Тэги'


class Ingredient(models.Model):
    name = models.CharField(max_length=200)
    measurement_unit = models.CharField(max_length=200)


class Content(models.Model):
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        related_name='contents'
    )
    recipe = models.ForeignKey(
        'Recipe',
        on_delete=models.CASCADE,
        related_name='contents'
    )
    amount = models.IntegerField(
        default=1, validators=[MinValueValidator(1)])


class Favorite(models.Model):
    siteuser = models.ForeignKey(
        User,
        related_name='favorites',
        on_delete=models.CASCADE,
        verbose_name='Пользователь',
    )
    recipe = models.ForeignKey(
        'Recipe',
        related_name='favoriters',
        on_delete=models.CASCADE,
        verbose_name='Подборка рецептов'
    )

    class Meta:
        unique_together = ('siteuser', 'recipe',)

    @property
    def is_owner(self, user):
        return self.siteuser == user


class Shoppingcart(models.Model):
    siteuser = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='shoppingcarts',
        verbose_name='Пользователь',
    )
    recipe = models.ForeignKey(
        'Recipe',
        on_delete=models.CASCADE,
        blank=True,
        related_name='shoppingcarts',
        verbose_name='Список рецептов для закупки ингредиентов'
    )

    class Meta:
        unique_together = ('siteuser', 'recipe',)

    @property
    def is_owner(self, user):
        return self.siteuser == user


class Recipe(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='recipes',
        verbose_name='Автор рецепта',
    )
    name = models.CharField(
        max_length=200,
        verbose_name='Название рецепта'
    )
    text = models.CharField(
        max_length=200,
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
        related_name='recipes'
    )
    image = models.ImageField(
        upload_to='recipes/images/',
        null=True,
        default=None
    )
    pub_date = models.DateTimeField(
        verbose_name='Дата публикации рецепта',
        auto_now_add=True,
        db_index=True
    )
    cooking_time = models.IntegerField(
        validators=[MinValueValidator],
        verbose_name='Время приготовления'
    )

    class Meta:
        ordering = ('pub_date',)
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'

    @property
    def is_author(self, user):
        return self.author == user
