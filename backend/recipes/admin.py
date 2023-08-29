from django.contrib import admin

from recipes.models import (Content, Favorite, Ingredient, Recipe,
                            Shoppingcart, Tag)
from users.models import Subscribe


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
