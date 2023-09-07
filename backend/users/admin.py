from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import Subscribe, User


class UserAdmin(UserAdmin):
    list_display = ('id', 'username', 'email', 'first_name', 'last_name',
                    'recipe_count', 'subscriber_count',)
    search_fields = ('username', 'email')

    def recipe_count(self, obj):
        return obj.recipes.count()

    def subscriber_count(self, obj):
        return obj.subscribers.count()


class SubscribeAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'author')


admin.site.register(User, UserAdmin)
admin.site.register(Subscribe, SubscribeAdmin)
