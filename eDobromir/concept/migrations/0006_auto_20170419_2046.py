# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-04-19 18:46
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('concept', '0005_auto_20170418_0038'),
    ]

    operations = [
        migrations.AlterField(
            model_name='concept',
            name='slug',
            field=models.SlugField(max_length=20),
        ),
    ]
