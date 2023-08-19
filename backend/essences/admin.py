from django.contrib import admin

from essences.models import (Content, Favorite, Ingredient, Recipe,
                             Shoppingcart, Subscribe, Tag)

""" Как настроить модель в админке
class TitleAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'name',
        'year',
        'category',
    )
    list_editable = ('category',)
    search_fields = ('name',)
    empty_value_display = '-пусто-'
"""


class ContentAdmin(admin.ModelAdmin):
    list_display = ('id', 'recipe', 'ingredient', 'amount',)


class IngredientAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'measurement_unit',)


class RecipeAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'author', 'name', 'text',
                    'cooking_time', 'image')


class SubscribeAdmin(admin.ModelAdmin):
    list_display = ('id', 'siteuser', 'author')


class FavoriteAdmin(admin.ModelAdmin):
    list_display = ('id', 'siteuser', 'recipe')


class ShoppingcartAdmin(admin.ModelAdmin):
    list_display = ('id', 'siteuser', 'recipe')


class TagAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'color', 'slug')


admin.site.register(Content, ContentAdmin)
admin.site.register(Favorite, FavoriteAdmin)
admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(Recipe, RecipeAdmin)
admin.site.register(Shoppingcart, ShoppingcartAdmin)
admin.site.register(Subscribe, SubscribeAdmin)
admin.site.register(Tag, TagAdmin)
