from django.contrib import admin
from .models import IPStore

# Register your models here.

class IPStoreAdmin(admin.ModelAdmin):
    list_display = ['ip', 'latitude', 'longitude', 'long_postal_code', 'nearest_address', 'added_on']
    ordering = ['-added_on']
    #list_filter = ['postal_code__country']

admin.site.register(IPStore, IPStoreAdmin)
