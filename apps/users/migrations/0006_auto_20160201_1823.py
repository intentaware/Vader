# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django_extensions.db.fields


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_visitor'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='added_on',
            field=django_extensions.db.fields.CreationDateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='date_joined',
            field=django_extensions.db.fields.CreationDateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='updated_on',
            field=django_extensions.db.fields.ModificationDateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='visitor',
            name='added_on',
            field=django_extensions.db.fields.CreationDateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='visitor',
            name='updated_on',
            field=django_extensions.db.fields.ModificationDateTimeField(auto_now=True),
        ),
    ]
