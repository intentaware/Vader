# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Column',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('parent_table_id', models.CharField(max_length=16)),
                ('column_id', models.CharField(max_length=16)),
                ('column_order', models.DecimalField(max_digits=4, decimal_places=1)),
                ('column_name', models.CharField(max_length=255)),
                ('indent_value', models.IntegerField(null=True, blank=True)),
                ('parent_column_id', models.CharField(max_length=255)),
                ('has_children', models.BooleanField()),
            ],
            options={
                'ordering': ('table__table_id', 'table__release', 'column_id'),
            },
        ),
        migrations.CreateModel(
            name='Geography',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('full_geoid', models.CharField(max_length=16)),
                ('full_name', models.CharField(max_length=128)),
                ('sumlev', models.CharField(max_length=3)),
                ('geo_type', models.CharField(max_length=24)),
                ('region', models.CharField(max_length=2, null=True, blank=True)),
                ('region_name', models.CharField(max_length=24, blank=True)),
                ('division', models.CharField(max_length=2, null=True, blank=True)),
                ('division_name', models.CharField(max_length=24, blank=True)),
                ('statefp', models.CharField(max_length=2, null=True, blank=True)),
                ('geoid', models.CharField(max_length=24, null=True, blank=True)),
                ('cd112fp', models.CharField(max_length=12, null=True, blank=True)),
                ('cdsessn', models.CharField(max_length=12, null=True, blank=True)),
                ('countyfp', models.CharField(max_length=12, null=True, blank=True)),
                ('placefp', models.CharField(max_length=12, null=True, blank=True)),
                ('classfp', models.CharField(max_length=12, blank=True)),
                ('sldlst', models.CharField(max_length=12, null=True, blank=True)),
                ('sldust', models.CharField(max_length=12, null=True, blank=True)),
                ('elsdlea', models.CharField(max_length=12, null=True, blank=True)),
                ('scsdlea', models.CharField(max_length=12, null=True, blank=True)),
                ('unsdlea', models.CharField(max_length=12, null=True, blank=True)),
                ('pcicbsa', models.CharField(max_length=1, null=True, blank=True)),
                ('pcinecta', models.CharField(max_length=1, null=True, blank=True)),
                ('csafp', models.CharField(max_length=12, null=True, blank=True)),
                ('cbsafp', models.CharField(max_length=12, null=True, blank=True)),
                ('metdivfp', models.CharField(max_length=12, null=True, blank=True)),
                ('zcta5ce10', models.CharField(max_length=12, null=True, blank=True)),
                ('name', models.CharField(max_length=128, blank=True)),
                ('namelsad', models.CharField(max_length=128, blank=True)),
                ('lsad', models.CharField(max_length=4, null=True, blank=True)),
                ('aland', models.CharField(max_length=24, null=True, blank=True)),
                ('intptlat', models.CharField(max_length=16, blank=True)),
                ('intptlon', models.CharField(max_length=16, blank=True)),
            ],
            options={
                'ordering': ('full_geoid',),
                'verbose_name_plural': 'Geographies',
            },
        ),
        migrations.CreateModel(
            name='SubjectConcept',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=128)),
                ('slug', models.SlugField()),
                ('census_category', models.CharField(default=b'Population', max_length=128, blank=True)),
                ('census_description', models.TextField(null=True, blank=True)),
                ('census_history', models.TextField(null=True, blank=True)),
                ('census_comparability', models.TextField(null=True, blank=True)),
                ('census_notes', models.TextField(null=True, blank=True)),
                ('description', models.TextField(null=True, blank=True)),
                ('source', models.CharField(default=b'American Community Survey Subject Definitions', max_length=64, null=True, blank=True)),
            ],
            options={
                'ordering': ('name',),
            },
        ),
        migrations.CreateModel(
            name='SummaryLevel',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('summary_level', models.CharField(max_length=3)),
                ('name', models.CharField(max_length=128)),
                ('slug', models.SlugField()),
                ('short_name', models.CharField(max_length=128, blank=True)),
                ('plural_name', models.CharField(max_length=128, blank=True)),
                ('description', models.TextField(blank=True)),
                ('census_description', models.TextField(blank=True)),
                ('census_code_description', models.TextField(blank=True)),
                ('census_notes', models.TextField(blank=True)),
                ('source', models.CharField(max_length=64, blank=True)),
                ('ancestors', models.ManyToManyField(related_name='descendants', to='census.SummaryLevel', blank=True)),
                ('parent', models.ForeignKey(related_name='children', blank=True, to='census.SummaryLevel', null=True)),
            ],
            options={
                'ordering': ('summary_level',),
            },
        ),
        migrations.CreateModel(
            name='Table',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('table_id', models.CharField(max_length=16)),
                ('table_name', models.CharField(max_length=255)),
                ('table_universe', models.CharField(max_length=512)),
                ('table_size', models.IntegerField()),
                ('subject_area', models.CharField(max_length=128)),
                ('topics', models.CharField(max_length=255, null=True, blank=True)),
                ('release', models.CharField(max_length=16)),
            ],
            options={
                'ordering': ('release', 'table_id'),
            },
        ),
        migrations.AddField(
            model_name='column',
            name='table',
            field=models.ForeignKey(to='census.Table'),
        ),
    ]
