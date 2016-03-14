# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations

def populate_data(apps, schemaeditor):
    Impression = apps.get_model('impressions', 'Impression')
    IPStore = apps.get_model('warehouse', 'IPStore')
    # print ''
    # from plugins.cities.models import Country, PostalCode

    # for i in Impression.objects.filter(meta__at_ip__isnull=False, meta__at_ip2geo__isnull=False):
    #     try:
    #         country_code = i.meta['ip2geo']['country']['iso_code']
    #         try:
    #             country = Country.objects.get(code=country_code)
    #         except Country.DoesNotExist:
    #             country = None
    #             print 'code %s does not exist in country database' %(country_code)
    #     except KeyError:
    #         country = None

    #     try:
    #         code = i.meta['ip2geo']['postal']['code']
    #         postal_code = PostalCode.objects.filter(
    #             code = code,
    #             country = country
    #         )
    #         if postal_code.count() > 0:
    #             postal_code_id = postal_code[0].id
    #             print postal_code_id
    #         else:
    #             postal_code_id = None

    #         ip, created = IPStore.objects.get_or_create(ip=i.meta['ip'])
    #         if postal_code_id:
    #             ip.postal_code_id=postal_code_id
    #             ip.save()
    #     except KeyError:
    #         print i.meta

def flush(apps, schemaeditor):
    print 'backwards'


class Migration(migrations.Migration):

    dependencies = [
        ('warehouse', '0003_auto_20151121_0652'),
    ]

    operations = [
        migrations.RunPython(populate_data, flush)
    ]
