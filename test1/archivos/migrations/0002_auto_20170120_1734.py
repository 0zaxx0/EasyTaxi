# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-01-20 17:34
from __future__ import unicode_literals

import archivos.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('archivos', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='document',
            name='filename',
        ),
        migrations.AlterField(
            model_name='document',
            name='docfile',
            field=models.FileField(upload_to=archivos.models.nombre),
        ),
    ]
