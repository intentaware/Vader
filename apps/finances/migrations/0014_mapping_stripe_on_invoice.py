# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-03-08 07:03
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('finances', '0013_auto_20160307_1524'),
    ]

    operations = [
        migrations.AlterField(
            model_name='invoice',
            name='stripe_id',
            field=models.CharField(blank=True, help_text=b'id obtained from stripe', max_length=256, null=True),
        ),
        migrations.AlterField(
            model_name='plan',
            name='amount',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=20),
        ),
        migrations.AlterField(
            model_name='plan',
            name='duration',
            field=models.IntegerField(choices=[(0, b'untill expiry'), (1, b'day'), (2, b'week'), (3, b'month'), (4, b'year')], default=0),
        ),
    ]