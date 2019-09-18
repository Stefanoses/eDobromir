# -*- coding: utf-8 -*-
from django.db import models
from django.utils.translation import ugettext_lazy as _
from taggit.managers import TaggableManager, _TaggableManager
from taggit.models import TagBase, GenericTaggedItemBase
from notification.models import FollowersModel
from django.contrib.auth.models import User
from django_extensions.db.models import TimeStampedModel
from fontawesome.fields import IconField


class DefaultTaggableManager(_TaggableManager):
    def add(self, *tags):
        super(DefaultTaggableManager, self).add(*tags)


class DefaultTag(TagBase, FollowersModel):
    icon = models.CharField(max_length=20, default='#')

    class Meta:
        verbose_name = _("Tag")
        verbose_name_plural = _("Tags")


class DefaultTagged(GenericTaggedItemBase):
    tag = models.ForeignKey(DefaultTag, related_name="%(app_label)s_%(class)s_items")


class TagsModel(models.Model):
    tags = TaggableManager(verbose_name='Tagi', through=DefaultTagged, manager=DefaultTaggableManager, blank=True)

    class Meta:
        abstract = True


class Sympathizer(TimeStampedModel, FollowersModel):
    created_by = models.ForeignKey(User)
    name = models.CharField(max_length=20, verbose_name='Nazwa', unique=True)
    slug = models.SlugField(max_length=20, unique=True)
    icon = IconField(verbose_name='Ikona', default='exclamation', blank=True)

    def __str__(self):
        return self.name


class SympathizerModel(models.Model):
    sympathizers = models.ForeignKey(Sympathizer, verbose_name='Sympatycy', blank=True, null=True)

    class Meta:
        abstract = True