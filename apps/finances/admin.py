from django.contrib import admin

from .models import *


class InvoiceAdmin(admin.ModelAdmin):
    list_display = [f.name for f in Invoice._meta.fields]

admin.site.register(Invoice, InvoiceAdmin)
admin.site.register(Module)
admin.site.register(Plan)
admin.site.register(PlanModule)
