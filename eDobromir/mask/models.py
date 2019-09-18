from __future__ import unicode_literals
from django.db import models
from django_extensions.db.models import TimeStampedModel
from datetime import datetime


class DeleteObjectsManager(models.Manager):
    def get_queryset(self):
        return super(DeleteObjectsManager, self).get_queryset().filter(mask__is_delete=False)

    def get_queryset_with_delete(self):
        return super(DeleteObjectsManager, self).get_queryset()


class DeleteMask(TimeStampedModel):
    is_delete = models.BooleanField(default=False)
    delete_set_datetime = models.DateTimeField(blank=True, null=True)

    def set_delete(self, state):
        self.is_delete = state
        self.delete_set_datetime = datetime.now()
        self.save()

    def delete(self, using=None, keep_parents=False):
        self.set_delete(True)
        self.save()


class DeleteMaskModel(models.Model):
    mask = models.ForeignKey(DeleteMask)
    objects = DeleteObjectsManager()

    def delete(self, using=None, keep_parents=False):
        self.mask.delete(using=None, keep_parents=False)

    class Meta:
        abstract = True


class DeleteMaskModelWithPrefix(DeleteMaskModel):
    mask_objects = DeleteObjectsManager()

    class Meta:
        abstract = True