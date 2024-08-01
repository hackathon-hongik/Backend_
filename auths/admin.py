from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _

from .models import CustomUser

class UserAdmin(BaseUserAdmin):
    ordering = ['email']
    list_display = ['email', 'nickname', 'is_staff', 'is_active']
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Personal info'), {'fields': ('nickname',)}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'nickname', 'password1', 'password2'),
        }),
    )
    search_fields = ('email', 'nickname')

admin.site.register(CustomUser, UserAdmin)
