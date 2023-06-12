from django.contrib import admin

from essences.models import Favorite, Ingredient, Subscribe, Tag

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


class SubscribeAdmin(admin.ModelAdmin):
    list_display = ('siteuser', 'author')


admin.site.register(Favorite)
admin.site.register(Ingredient)
admin.site.register(Subscribe, SubscribeAdmin)
admin.site.register(Tag)
# admin.site.register(Title, TitleAdmin)
