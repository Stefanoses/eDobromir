# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.db import models
from taggit.models import TaggedItem
from ckeditor_uploader.fields import RichTextUploadingField
from django.contrib.auth.models import User
from django_extensions.db.models import TimeStampedModel
from django.core.validators import URLValidator
from sortedm2m.fields import SortedManyToManyField
from datetime import datetime
from imagekit.models import ImageSpecField
from imagekit.processors import SmartResize
from comments.models import Comment
from comments.models import CommentsModel
from votes.models import VoteModel
from django.db.models.signals import pre_save
from administration.models import BehaviorSettings
from django.conf import settings
from django.shortcuts import get_object_or_404
from tags.models import TagsModel, SympathizerModel
from linked.models import LinkedModel
from moderation.models import ModerationModel
from diary.models import DiaryModel
from mask.models import DeleteMaskModel
from favorites.models import FavoriteModel
from django.core.validators import MinValueValidator, MaxValueValidator


class Eureka(TimeStampedModel, CommentsModel, VoteModel, TagsModel, LinkedModel, ModerationModel, DiaryModel, DeleteMaskModel, FavoriteModel, SympathizerModel):
    title = models.CharField(max_length=80, verbose_name='Tytuł')
    description = models.TextField(max_length=300, verbose_name='Opis')
    link = models.CharField(max_length=255, validators=[URLValidator()], verbose_name='Link do instrukcji, filmu lub źródła np.: http://www.', blank=True)
    content_type = models.CharField(max_length=9, choices=(
        ('0', 'Autorska'),
        ('1', 'Cudza')
    ), default='0', verbose_name='Typ treści')
    preview_image = models.ImageField(upload_to='preview_images', verbose_name='Miniaturka')
    preview_image_thumbnail = ImageSpecField(source='preview_image', processors=[SmartResize(180, 100)], format='JPEG', options={'quality':100})

    eurekaInstruction = models.ForeignKey('EurekaInstruction')

    is_waiting = models.BooleanField(default=True)
    is_published = models.BooleanField(default=False)

    published = models.DateTimeField(verbose_name='Opublikowano', blank=True, null=True)

    slug = models.SlugField(max_length=20)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Stworzone przez')
    difficult = models.CharField(choices=(('easy', 'Łatwy'), ('medium', 'Średni'), ('hard', 'Trudny')), verbose_name='Poziom trudności', blank=True, max_length=20)
    price = models.PositiveIntegerField(verbose_name='Cena orientacyjna (PLN)', blank=True, default=0, validators=[MaxValueValidator(999999)])

    def get_absolute_url(self):
        return "/eureka/{}/".format(self.slug)

    def publish(self):
        self.is_published = True
        self.published = datetime.now()
        self.save()

    class Meta:
        permissions = (
            ('is_owner', 'Is owner eureka'),
            ('can_vote', 'Can votes eureka'),
            ('can_view', 'Can view eureka'),
        )

class EurekaInstruction(TimeStampedModel):
    steps = SortedManyToManyField('EurekaInstructionStep')

class EurekaInstructionStep(TimeStampedModel):
    title = models.CharField(max_length=40, verbose_name='Tytuł kroku')
    content = RichTextUploadingField(config_name='instruction_ckeditor', verbose_name='Treść kroku', blank=True)
    step_slug = models.SlugField(max_length=10)