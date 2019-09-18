# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django_extensions.db.models import TimeStampedModel
from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType


class FavoriteModel(models.Model):
    favorites = models.ManyToManyField(User, blank=True, related_name='%(app_label)s_%(class)s_favorites')

    class Meta:
        abstract = True