# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-02-02 19:45
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('winn', '0009_auto_20170202_1549'),
    ]

    operations = [
        migrations.AlterField(
            model_name='historicobienvenida',
            name='date',
            field=models.DateField(auto_now_add=True, verbose_name='Date'),
        ),
    ]
