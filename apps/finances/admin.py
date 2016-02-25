from django.contrib import admin

from .models import *


class InvoiceAdmin(admin.ModelAdmin):
    list_display = [f.name for f in Invoice._meta.fields]

class ModuleAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'segment']

admin.site.register(Invoice, InvoiceAdmin)
admin.site.register(Module, ModuleAdmin)
admin.site.register(Plan)
admin.site.register(PlanModule)
