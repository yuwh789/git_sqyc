# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sqyc_bi', '0006_auto_20180525_1142'),
    ]

    operations = [
        migrations.CreateModel(
            name='t_rec_table',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID', auto_created=True)),
                ('the_name', models.CharField(max_length=100)),
                ('comment', models.CharField(max_length=200)),
                ('other', models.CharField(max_length=200)),
                ('update_date', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.DeleteModel(
            name='t_experience',
        ),
    ]
