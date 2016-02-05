# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django_extensions.db.fields


class Migration(migrations.Migration):

    dependencies = [
        ('impressions', '0016_auto_20151127_0633'),
    ]

    operations = [
        migrations.AlterField(
            model_name='impression',
            name='added_on',
            field=django_extensions.db.fields.CreationDateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='impression',
            name='updated_on',
            field=django_extensions.db.fields.ModificationDateTimeField(auto_now=True),
        ),
    ]
