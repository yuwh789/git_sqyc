# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sqyc_bi', '0005_t_company_day_data_t_experience'),
    ]

    operations = [
        migrations.AlterField(
            model_name='t_company_day_data',
            name='t_date',
            field=models.DateField(),
        ),
    ]
