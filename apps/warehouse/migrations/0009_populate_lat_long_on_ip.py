# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations

def populate(apps, schemaeditor):
    from apps.impressions.models import Impression
    from apps.warehouse.models import IPStore

    print ''

    for ip in IPStore.objects.all():
        print 'importing data for %s' %(ip.ip)
        impression = Impression.objects.filter(meta__at_ip=ip).order_by('-added_on')[0]
        location = impression.meta['ip2geo']['location']
        ip.latitude = location['latitude']
        ip.longitude = location['longitude']
        from googlemaps import Client
        from django.conf import settings
        import json
        gmaps = Client(key=settings.GOOGLE_GEOCODE_KEY)
        result = gmaps.reverse_geocode((location['latitude'], location['longitude']))
        ip.geocode = json.dumps(result)
        ip.save()

def reverse(apps, schemaeditor):
    pass


class Migration(migrations.Migration):

    dependencies = [
        ('warehouse', '0008_ipstore_census'),
    ]

    operations = [
        migrations.RunPython(populate, reverse)
    ]
