from django.contrib import admin

from .models import *


class CompanyAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'name',
        'publisher_key',
        'is_publisher',
        'is_advertiser',
        'is_active',
        'advertiser_rate',
        'publisher_rate',
    ]
    list_display_links = ['id', 'name', 'publisher_key', ]
    ordering = ['id', ]


class CompanyGroupAdmin(admin.ModelAdmin):
    list_display = [f.name for f in CompanyGroup._meta.fields]


class CompanyUserAdmin(admin.ModelAdmin):
    list_display = [f.name for f in CompanyUser._meta.fields]


admin.site.register(Company, CompanyAdmin)
admin.site.register(CompanyGroup, CompanyGroupAdmin)
admin.site.register(CompanyUser, CompanyUserAdmin)
admin.site.register(CompanySubscription)
