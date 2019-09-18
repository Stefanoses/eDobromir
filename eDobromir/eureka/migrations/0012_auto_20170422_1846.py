# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-04-22 16:46
from __future__ import unicode_literals

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('eureka', '0011_auto_20170422_1845'),
    ]

    operations = [
        migrations.AlterField(
            model_name='eureka',
            name='price',
            field=models.PositiveIntegerField(blank=True, default=0, max_length=5, validators=[django.core.validators.MaxValueValidator(999999)], verbose_name='Cena orientacyjna (PLN)'),
        ),
    ]
