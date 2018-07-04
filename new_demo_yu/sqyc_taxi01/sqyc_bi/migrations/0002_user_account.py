# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sqyc_bi', '0001_initial'),
    ]

    operations = [
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
    ]
