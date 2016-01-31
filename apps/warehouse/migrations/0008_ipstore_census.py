# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django_pgjson.fields


class Migration(migrations.Migration):

    dependencies = [
        ('warehouse', '0007_ipstore_geocode'),
    ]

    operations = [
        migrations.AddField(
            model_name='ipstore',
            name='census',
            field=django_pgjson.fields.JsonBField(null=True, blank=True),
        ),
    ]
