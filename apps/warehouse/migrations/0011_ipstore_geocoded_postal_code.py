# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-04-11 14:31
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('warehouse', '0010_auto_20160223_1956'),
    ]

    operations = [
        migrations.AddField(
            model_name='ipstore',
            name='geocoded_postal_code',
            field=models.CharField(blank=True, max_length=8, null=True),
        ),
    ]
