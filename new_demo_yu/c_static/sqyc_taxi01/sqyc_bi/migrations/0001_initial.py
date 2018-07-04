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
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('city_id', models.IntegerField()),
                ('city_name', models.CharField(max_length=20)),
                ('driver_id', models.IntegerField()),
                ('driver_name', models.CharField(max_length=20)),
                ('driver_phone', models.CharField(max_length=12)),
                ('company_name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='t_company_day_data',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('t_date', models.DateField()),
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
            name='t_driver_order_num',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_date', models.DateField()),
                ('order_status', models.CharField(max_length=10)),
                ('recmd_status', models.CharField(max_length=10)),
                ('one_num', models.CharField(max_length=10)),
                ('two_num', models.CharField(max_length=10)),
                ('three_num', models.CharField(max_length=10)),
                ('four_num', models.CharField(max_length=10)),
                ('five_seven_num', models.CharField(max_length=10)),
                ('eight_ten_num', models.CharField(max_length=10)),
                ('gt_eleven_num', models.CharField(max_length=10)),
                ('update_date', models.DateField(auto_now=True)),
            ],
            options={
                'db_table': 't_driver_order_num',
            },
        ),
        migrations.CreateModel(
            name='t_experience',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='user_account',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_name', models.CharField(max_length=20)),
                ('password', models.CharField(max_length=40)),
                ('phone', models.CharField(max_length=30)),
                ('comment', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='UserManager',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
    ]
