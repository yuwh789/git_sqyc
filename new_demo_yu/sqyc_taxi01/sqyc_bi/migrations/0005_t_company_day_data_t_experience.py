# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sqyc_bi', '0004_t_driver_order_num'),
    ]

    operations = [
        migrations.CreateModel(
            name='t_company_day_data',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('t_date', models.CharField(max_length=20)),
                ('city', models.CharField(max_length=30)),
                ('city_id', models.IntegerField()),
                ('driver_id', models.IntegerField()),
                ('driver_name', models.CharField(max_length=30)),
                ('driver_phone', models.CharField(max_length=30)),
                ('taxi_company_id', models.IntegerField()),
                ('taxi_company_name', models.CharField(max_length=30)),
                ('com_cnt', models.IntegerField()),
                ('reward_punish_money', models.FloatField()),
                ('plate_number', models.CharField(max_length=30)),
                ('id_number', models.CharField(max_length=30)),
                ('total_online_minute', models.IntegerField()),
                ('update_date', models.DateField()),
            ],
            options={
                'db_table': 't_company_day_data',
            },
        ),
        migrations.CreateModel(
            name='t_experience',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
    ]
