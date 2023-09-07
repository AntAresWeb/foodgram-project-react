from django.contrib import admin
from django.forms import ValidationError
from django.forms.models import BaseInlineFormSet
from recipes.models import (Content, Favorite, Ingredient, Recipe,
                            Shoppingcart, Tag)


class ContentAdmin(admin.ModelAdmin):
    list_display = ('id', 'recipe', 'ingredient', 'amount',)


class IngredientAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'measurement_unit',)


class IngredientInlineFormSet(BaseInlineFormSet):
    def clean(self):
        super(IngredientInlineFormSet, self).clean()
        total = len(self.forms)
        for form in self.forms:
            content = form.cleaned_data
            if content.get('ingredient') is None or content.get('DELETE'):
                total -= 1
        if total < 1:
            raise ValidationError(
                'В рецепте должен использоваться хотя бы один ингредиент!')


class RecipeIngrdientsInline(admin.TabularInline):
    model = Content
    formset = IngredientInlineFormSet
    extra = 1


class RecipeAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'author', 'name', 'text',
                    'cooking_time', 'image', 'ingredients_list')
    inlines = (RecipeIngrdientsInline,)
    filter_horizontal = ('tags',)

    def ingredients_list(self, obj):
        return ','.join([ingr.name for ingr in obj.ingredients.all()])
    ingredients_list.short_description = 'Ингредиенты'


class FavoriteAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'recipe')


class ShoppingcartAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'recipe')


class TagAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'color', 'slug')


admin.site.register(Content, ContentAdmin)
admin.site.register(Favorite, FavoriteAdmin)
admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(Recipe, RecipeAdmin)
admin.site.register(Shoppingcart, ShoppingcartAdmin)
admin.site.register(Tag, TagAdmin)
