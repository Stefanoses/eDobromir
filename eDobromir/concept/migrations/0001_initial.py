# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-04-17 19:14
from __future__ import unicode_literals

import ckeditor_uploader.fields
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django_extensions.db.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('comments', '0001_initial'),
        ('diary', '0001_initial'),
        ('linked', '0001_initial'),
        ('mask', '0001_initial'),
        ('moderation', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Concept',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('vote_score', models.IntegerField(db_index=True, default=0)),
                ('num_vote_up', models.PositiveIntegerField(db_index=True, default=0)),
                ('num_vote_down', models.PositiveIntegerField(db_index=True, default=0)),
                ('created', django_extensions.db.fields.CreationDateTimeField(auto_now_add=True, verbose_name='created')),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(auto_now=True, verbose_name='modified')),
                ('content', ckeditor_uploader.fields.RichTextUploadingField(verbose_name='Tre\u015b\u0107 koncepcji')),
                ('slug', models.SlugField(max_length=20, unique=True)),
                ('published', models.DateTimeField(auto_now_add=True, verbose_name='Opublikowano')),
                ('comments', models.ManyToManyField(to='comments.Comment', verbose_name='Komentarze')),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Stworzone przez')),
                ('diarys', models.ManyToManyField(to='diary.Diary')),
                ('favorites', models.ManyToManyField(blank=True, related_name='concept_concept_favorites', to=settings.AUTH_USER_MODEL)),
                ('links', models.ManyToManyField(to='linked.Linked', verbose_name='Powi\u0105zane')),
                ('mask', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mask.DeleteMask')),
                ('moderations', models.ManyToManyField(to='moderation.Moderation')),
            ],
            options={
                'permissions': (('is_owner', 'Is owner concept'), ('can_vote', 'Can votes concept')),
            },
        ),
    ]
