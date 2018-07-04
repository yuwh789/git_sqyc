# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sqyc_bi', '0003_usermanager'),
    ]

    operations = [
        migrations.CreateModel(
            name='t_driver_order_num',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, auto_created=True, verbose_name='ID')),
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
    ]
