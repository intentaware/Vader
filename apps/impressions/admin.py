from django.contrib import admin
from import_export import resources, admin as ie_admin

from .models import Impression

class ImpressionResource(resources.ModelResource):
    model = Impression


class ImpressionAdmin(ie_admin.ExportActionModelAdmin):
    list_display = [f.name for f in Impression._meta.fields]
    list_filter = ['campaign__name', 'publisher__name', 'visitor']
    resource_class = ImpressionResource
    pass


admin.site.register(Impression, ImpressionAdmin)
