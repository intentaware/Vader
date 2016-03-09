from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as AuthUserAdmin
from django.utils.translation import ugettext, ugettext_lazy as _
from .models import *


class UserAdmin(AuthUserAdmin):
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal Info', {
            'classes': ('wide', ),
            'fields': ('first_name', 'last_name')}
            ),
        ('Important dates', {'fields': ('last_login',)}),
    )
    add_fieldsets = (
        (
            None, {
                'classes': ('wide', ),
                'fields': ('email', 'password1', 'password2'),
            }
        ),
    )
    list_display = ('email', 'first_name', 'last_name', 'is_staff', )
    list_filter = ('is_staff', 'is_superuser', 'is_active', )
    search_fields = ('email', )
    ordering = ['id', 'email']
    filter_horizontal = ('groups', 'user_permissions', )


admin.site.register(User, UserAdmin)
