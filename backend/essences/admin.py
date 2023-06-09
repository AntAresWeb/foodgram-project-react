from django.contrib import admin

from essences.models import Ingredient, Tag

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

admin.site.register(Ingredient)
admin.site.register(Tag)
# admin.site.register(Title, TitleAdmin)
