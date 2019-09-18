# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from django.db import models
from django_extensions.db.models import TimeStampedModel
from django.contrib.auth.models import User
from mptt.models import MPTTModel, TreeForeignKey
from ckeditor_uploader.fields import RichTextUploadingField
from tools.models import IpStampedModel
from votes.models import VoteModel
from moderation.models import ModerationModel
from mask.models import DeleteMaskModelWithPrefix


class Comment(MPTTModel, TimeStampedModel, VoteModel, ModerationModel, DeleteMaskModelWithPrefix):
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Stworzone przez')
    parent = TreeForeignKey('self', related_name='children', null=True, db_index=True, blank=True)
    content = RichTextUploadingField(config_name='description_ckeditor', verbose_name='Treść komentarza', max_length=2000)
    slug = models.SlugField(unique=True, max_length=10)


class CommentsModel(models.Model):
    comments = models.ManyToManyField(Comment, verbose_name='Komentarze', blank=True)

    class Meta:
        abstract = True