# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django_extensions.db.models import TimeStampedModel
from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType


class FollowersModel(models.Model):
    observers = models.ManyToManyField(User)


class FollowersUserModel(models.Model):
    container = models.ManyToManyField(User)
    user = models.OneToOneField(User, related_name='observers', on_delete=models.CASCADE)


class Notification(TimeStampedModel):
    content = models.CharField(verbose_name='Treść', max_length=100)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    seeed_first = models.BooleanField(default=False)
    seeed_second = models.BooleanField(default=False)


class NotificationModel(models.Model):
    user = models.OneToOneField(User, related_name='notifications', on_delete=models.CASCADE)
    container = models.ManyToManyField(Notification)

    def eureka_on_main_page(self, content_object):
        self.container.create(content='Twoja eureka jest na stronie głównej', content_object=content_object)

    def eureka_comment(self, content_object):
        self.container.create(content='Twoja eureka została skomentowana', content_object=content_object)

    def concpet_comment(self, content_object):
        self.container.create(content='Twoja koncepcja została skomentowana', content_object=content_object)

    def user_comment(self, content_object):
        self.container.create(content='Dostałeś odpowiedź w komentarzu', content_object=content_object)

    def user_observe(self, content_object):
        self.container.create(content='Użytkownik którego obserwujesz dodał treść', content_object=content_object)

    def tag_observe(self, content_object):
        self.container.create(content='Ktoś dodał treść w tagu który obserwujesz', content_object=content_object)

    def enthusiasts_observe(self, content_object):
        self.container.create(content='Ktoś dodał treść w entuzjastach których obserwujesz', content_object=content_object)


class Message(TimeStampedModel):
    sender = models.ForeignKey(User, verbose_name='Nadawca', related_name='sender')
    recipient = models.ForeignKey(User, verbose_name='Odbiorca', related_name='recipient')
    content = models.TextField(max_length=1000, verbose_name='Treść')
    conversation = models.ForeignKey('Conversation', related_name='conversation')


class Conversation(TimeStampedModel):
    owners = models.ManyToManyField(User, related_name='owners')
    messages = models.ManyToManyField(Message, related_name='messages')
    seeed = models.ManyToManyField(User, related_name='seeed', blank=True)