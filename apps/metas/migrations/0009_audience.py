# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django_pgjson.fields
import django_extensions.db.fields


class Migration(migrations.Migration):

    dependencies = [
        ('companies', '0021_auto_20160201_1823'),
        ('metas', '0008_auto_20160201_1823'),
    ]

    operations = [
        migrations.CreateModel(
            name='Audience',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('added_on', django_extensions.db.fields.CreationDateTimeField(auto_now_add=True)),
                ('updated_on', django_extensions.db.fields.ModificationDateTimeField(auto_now=True)),
                ('meta', django_pgjson.fields.JsonBField(default={})),
                ('company', models.ForeignKey(related_name='audiences', blank=True, to='companies.Company', null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
