# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='sqyc_table',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, primary_key=True, verbose_name='ID')),
                ('city_id', models.IntegerField()),
                ('city_name', models.CharField(max_length=20)),
                ('driver_id', models.IntegerField()),
                ('driver_name', models.CharField(max_length=20)),
                ('driver_phone', models.CharField(max_length=12)),
                ('company_name', models.CharField(max_length=100)),
            ],
        ),
    ]
