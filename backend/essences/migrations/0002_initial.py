# Generated by Django 3.2.16 on 2023-06-08 16:33

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('essences', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='subcscribe',
            name='siteuser',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Подписчик'),
        ),
        migrations.AddField(
            model_name='subcscribe',
            name='subscribe',
            field=models.ManyToManyField(blank=True, related_name='subscruber', to=settings.AUTH_USER_MODEL, verbose_name='Подписка на авторов'),
        ),
        migrations.AddField(
            model_name='shoppingcart',
            name='recipe',
            field=models.ManyToManyField(blank=True, related_name='shopingcart', to='essences.Recipe', verbose_name='Список рецептов для закупки ингредиентов'),
        ),
        migrations.AddField(
            model_name='shoppingcart',
            name='siteuser',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Пользователь'),
        ),
        migrations.AddField(
            model_name='recipe',
            name='author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='recipe', to=settings.AUTH_USER_MODEL, verbose_name='Автор рецепта'),
        ),
        migrations.AddField(
            model_name='recipe',
            name='tag',
            field=models.ManyToManyField(blank=True, related_name='recipe', to='essences.Tag', verbose_name='Список тегов'),
        ),
        migrations.AddField(
            model_name='favorite',
            name='recipe',
            field=models.ManyToManyField(blank=True, related_name='favorite', to='essences.Recipe', verbose_name='Подборка рецептов'),
        ),
        migrations.AddField(
            model_name='favorite',
            name='siteuser',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Пользователь'),
        ),
        migrations.AddField(
            model_name='content',
            name='igredient',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='essences.ingredient'),
        ),
        migrations.AddField(
            model_name='content',
            name='recipe',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='content', to='essences.recipe'),
        ),
    ]
