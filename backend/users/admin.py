from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User


@admin.register(User)
class UserAdmin(UserAdmin):
    list_display = ('id', 'username', 'email', 'first_name', 'last_name',
                    'recipe_count', 'subscriber_count',)
    search_fields = ('username', 'email')

    def recipe_count(self, obj):
        return obj.recipes.count()

    def subscriber_count(self, obj):
        return obj.subscribers.count()
