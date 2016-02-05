# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django_extensions.db.fields


class Migration(migrations.Migration):

    dependencies = [
        ('warehouse', '0008_ipstore_census'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ipstore',
            name='added_on',
            field=django_extensions.db.fields.CreationDateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='ipstore',
            name='updated_on',
            field=django_extensions.db.fields.ModificationDateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='postaldemographics',
            name='added_on',
            field=django_extensions.db.fields.CreationDateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='postaldemographics',
            name='updated_on',
            field=django_extensions.db.fields.ModificationDateTimeField(auto_now=True),
        ),
    ]
