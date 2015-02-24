# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('companies', '0007_auto_20150220_1312'),
    ]

    operations = [
        migrations.AddField(
            model_name='company',
            name='users',
            field=models.ManyToManyField(to=settings.AUTH_USER_MODEL, through='companies.CompanyUser'),
            preserve_default=True,
        ),
    ]