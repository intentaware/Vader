# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django_extensions.db.fields


class Migration(migrations.Migration):

    dependencies = [
        ('finances', '0006_plan_matric_unit'),
    ]

    operations = [
        migrations.AlterField(
            model_name='invoice',
            name='added_on',
            field=django_extensions.db.fields.CreationDateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='invoice',
            name='updated_on',
            field=django_extensions.db.fields.ModificationDateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='plan',
            name='added_on',
            field=django_extensions.db.fields.CreationDateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='plan',
            name='updated_on',
            field=django_extensions.db.fields.ModificationDateTimeField(auto_now=True),
        ),
    ]
