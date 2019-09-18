# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.db import models
from taggit.models import TaggedItem
from ckeditor_uploader.fields import RichTextUploadingField
from django.contrib.auth.models import User
from django_extensions.db.models import TimeStampedModel
from comments.models import Comment
from comments.models import CommentsModel
from votes.models import VoteModel
from administration.models import BehaviorSettings
from tags.models import TagsModel, SympathizerModel
from linked.models import LinkedModel
from moderation.models import ModerationModel
from diary.models import DiaryModel
from mask.models import DeleteMaskModel
from favorites.models import FavoriteModel


class Concept(TimeStampedModel, CommentsModel, VoteModel, TagsModel, LinkedModel, ModerationModel, DiaryModel, DeleteMaskModel, FavoriteModel, SympathizerModel):
    content = RichTextUploadingField(config_name='instruction_ckeditor', verbose_name='Treść koncepcji')

    slug = models.SlugField(max_length=20)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Stworzone przez')
    published = models.DateTimeField(verbose_name='Opublikowano', auto_now_add=True)

    def get_absolute_url(self):
        return "/concept/{}/".format(self.slug)

    class Meta:
        permissions = (
            ('is_owner', 'Is owner concept'),
            ('can_vote', 'Can votes concept'),
        )