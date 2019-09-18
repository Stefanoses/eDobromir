# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-04-17 22:38
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('concept', '0004_auto_20170417_2118'),
    ]

    operations = [
        migrations.AlterField(
            model_name='concept',
            name='comments',
            field=models.ManyToManyField(blank=True, to='comments.Comment', verbose_name='Komentarze'),
        ),
        migrations.AlterField(
            model_name='concept',
            name='diarys',
            field=models.ManyToManyField(blank=True, to='diary.Diary'),
        ),
        migrations.AlterField(
            model_name='concept',
            name='links',
            field=models.ManyToManyField(blank=True, to='linked.Linked', verbose_name='Powi\u0105zane'),
        ),
        migrations.AlterField(
            model_name='concept',
            name='moderations',
            field=models.ManyToManyField(blank=True, to='moderation.Moderation'),
        ),
    ]
