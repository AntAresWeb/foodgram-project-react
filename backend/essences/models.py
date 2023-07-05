from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator

User = get_user_model()


class Tag(models.Model):
    name = models.CharField(max_length=200)
    color = models.CharField(max_length=7, blank=True)
    slug = models.SlugField(max_length=200, blank=True)


class Ingredient(models.Model):
    name = models.CharField(max_length=200)
    measurement_unit = models.CharField(max_length=200)


class Content(models.Model):
    ingredient = models.ForeignKey(
        Ingredient, related_name='contents', on_delete=models.CASCADE)
    recipe = models.ForeignKey(
        'Recipe', related_name='contents', on_delete=models.CASCADE)
    amount = models.IntegerField(default=1, validators=[MinValueValidator(1)])


class Subscribe(models.Model):
    siteuser = models.ForeignKey(
        User,
        related_name='subscribes',
        on_delete=models.CASCADE,
        verbose_name='Подписчик',
    )
    author = models.ForeignKey(
        User,
        related_name='subscribers',
        on_delete=models.CASCADE,
        verbose_name='Подписка на автора'
    )


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


class Shoppingcart(models.Model):
    siteuser = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Пользователь',
    )
    recipe = models.ManyToManyField(
        'Recipe',
        blank=True,
        related_name='shopingcart',
        verbose_name='Список рецептов для закупки ингредиентов'
    )


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
