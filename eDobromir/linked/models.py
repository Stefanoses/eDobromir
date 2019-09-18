# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django_extensions.db.models import TimeStampedModel
from votes.models import VoteModel
from django.contrib.auth.models import User
from mask.models import DeleteMaskModel


class Linked(TimeStampedModel, VoteModel, DeleteMaskModel):
    title = models.CharField(max_length=20, verbose_name='Tytuł')
    link = models.URLField(verbose_name='Link')
    slug = models.SlugField(max_length=20)
    created_by = models.ForeignKey(User)


class LinkedModel(models.Model):
    links = models.ManyToManyField(Linked, verbose_name='Powiązane', blank=True)

    class Meta:
        abstract = True
