from __future__ import unicode_literals
from django.db import models
from django_extensions.db.models import TimeStampedModel, CreationDateTimeField


class Diary(TimeStampedModel):
    ip = models.CharField(max_length=40)
    session = models.CharField(max_length=40)


class DiaryModel(models.Model):
    diarys = models.ManyToManyField(Diary, blank=True)

    class Meta:
        abstract = True
