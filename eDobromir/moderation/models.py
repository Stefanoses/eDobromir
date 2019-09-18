from __future__ import unicode_literals

from django.db import models
from django_extensions.db.models import TimeStampedModel
from django.contrib.auth.models import User


class Moderation(TimeStampedModel):
    created_by = models.ForeignKey(User)
    choiceReason = models.CharField(max_length=100)
    reason = models.TextField(verbose_name='Uzasadnienie', max_length=300)


class ModerationModel(models.Model):
    moderations = models.ManyToManyField(Moderation, blank=True)

    class Meta:
        abstract = True