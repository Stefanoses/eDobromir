# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-04-23 12:07
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('notification', '0007_auto_20170423_1405'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='conversation',
            name='messages',
        ),
        migrations.RemoveField(
            model_name='message',
            name='converstion',
        ),
        migrations.RemoveField(
            model_name='message',
            name='recipient',
        ),
        migrations.RemoveField(
            model_name='message',
            name='sender',
        ),
        migrations.DeleteModel(
            name='Conversation',
        ),
        migrations.DeleteModel(
            name='Message',
        ),
    ]
