# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-02-23 19:51
from __future__ import unicode_literals

import django.contrib.postgres.fields.jsonb
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('finances', '0007_auto_20160201_1823'),
    ]

    operations = [
        migrations.AlterField(
            model_name='invoice',
            name='gateway_response',
            field=django.contrib.postgres.fields.jsonb.JSONField(default={}),
        ),
    ]