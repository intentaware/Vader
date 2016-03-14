# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django_extensions.db.fields


class Migration(migrations.Migration):

    dependencies = [
        ('guages', '0005_update_related_names_on_metric'),
    ]

    operations = [
        migrations.AlterField(
            model_name='asset',
            name='added_on',
            field=django_extensions.db.fields.CreationDateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='asset',
            name='updated_on',
            field=django_extensions.db.fields.ModificationDateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='metric',
            name='added_on',
            field=django_extensions.db.fields.CreationDateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='metric',
            name='updated_on',
            field=django_extensions.db.fields.ModificationDateTimeField(auto_now=True),
        ),
    ]
