# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('metas', '0010_campaignaudience'),
    ]

    operations = [
        migrations.AddField(
            model_name='campaignaudience',
            name='audience',
            field=models.ForeignKey(default=1, to='metas.Audience'),
        ),
    ]
