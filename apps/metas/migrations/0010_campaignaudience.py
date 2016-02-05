# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django_extensions.db.fields


class Migration(migrations.Migration):

    dependencies = [
        ('campaigns', '0020_auto_20160201_1823'),
        ('metas', '0009_audience'),
    ]

    operations = [
        migrations.CreateModel(
            name='CampaignAudience',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('added_on', django_extensions.db.fields.CreationDateTimeField(auto_now_add=True)),
                ('updated_on', django_extensions.db.fields.ModificationDateTimeField(auto_now=True)),
                ('campaign', models.ForeignKey(to='campaigns.Campaign')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
