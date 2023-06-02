from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User


@admin.register(User)
class RoleUserAdmin(UserAdmin):
    list_display = ('id', 'username', 'email', 'role', 'bio', 'first_name',
                    'last_name')
    search_fields = ('username',)
    list_editable = ('role',)
