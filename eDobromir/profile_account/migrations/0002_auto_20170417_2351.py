# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-04-17 21:51
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profile_account', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='settingsavatar',
            name='avatar_image',
            field=models.ImageField(default='default_images/avatar/light-bulb.png', upload_to='avatar_images', verbose_name='Avatar'),
        ),
    ]
