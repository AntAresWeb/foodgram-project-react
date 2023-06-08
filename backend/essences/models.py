from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Tag(models.Model):
    name = models.CharField(max_length=200)
    color = models.CharField(max_length=7, blank=True)
    slug = models.SlugField(max_length=200, blank=True)


class Ingredient(models.Model):
    name = models.CharField(max_length=200)
    measurement_unit = models.CharField(max_length=200)


class Content(models.Model):
    igredient = models.ForeignKey(Ingredient, )
    recipe = models.ForeignKey(
        'Recipe', related_name='content', on_delete=models.CASCADE)
    amount = models.IntegerField(min=1)


class Subcscribe(models.Model):
    ...


class Favorite(models.Model):
    ...


class Recipe(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='recipe',
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
    tag = models.ManyToManyField(
        Tag,
        related_name='recipe',
        blank=True,
        verbose_name='Список тегов'
    )
    content = models.ManyToManyField(
        Content,
        related_name='recipe',
        blank=True,
        verbose_name='Состав набора ингредиентов'
    )
    picture = models.ImageField(
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
        min=1, verbose_name='Время приготовления'
    )

    class Meta:
        ordering = ('-year',)
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'

    def __str__(self):
        self.name


class Shoppingcart(models.Model):
    ...




