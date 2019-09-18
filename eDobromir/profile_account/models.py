# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save
from guardian.shortcuts import assign_perm
from imagekit.processors import ResizeToFill, SmartResize
from imagekit.models import ImageSpecField
from django.db.models import Count
from notification.models import NotificationModel, FollowersModel, FollowersUserModel
from favorites.models import FavoriteModel


class SettingsProfile(models.Model):
    name = models.CharField(max_length=20, verbose_name='Imię', blank=True)
    last_name = models.CharField(max_length=20, verbose_name='Nazwisko', blank=True)
    public_email = models.EmailField(max_length=30, verbose_name='Publiczny email', blank=True)
    website = models.URLField(verbose_name='Strona www', blank=True)
    town = models.CharField(max_length=20, verbose_name='Miasto', blank=True)

    social_facebook = models.URLField(max_length=100, verbose_name='Facebook', blank=True)
    social_twitter = models.URLField(max_length=100, verbose_name='Twitter', blank=True)
    social_google_plus = models.URLField(max_length=100, verbose_name='Google plus', blank=True)
    social_linkedin = models.URLField(max_length=100, verbose_name='Linkedin', blank=True)
    social_youtube = models.URLField(max_length=100, verbose_name='YouTube', blank=True)

    description = models.TextField(max_length=300, verbose_name='Opis konta', blank=True)


class SettingsAvatar(models.Model):
    avatar_image = models.ImageField(upload_to='avatar_images', verbose_name='Avatar', default='default_images/avatar/light-bulb.png')
    avatar_image_profile = ImageSpecField(source='avatar_image',
                                          processors=[ResizeToFill(360, 360)],
                                          format='PNG',
                                          options={'quality': 100})
    avatar_image_comment = ImageSpecField(source='avatar_image',
                                          processors=[ResizeToFill(15, 15)],
                                          format='PNG',
                                          options={'quality': 60})
    avatar_image_concept = ImageSpecField(source='avatar_image',
                                          processors=[ResizeToFill(45, 45)],
                                          format='PNG',
                                          options={'quality': 60})


class Settings(models.Model):
    user = models.OneToOneField(User, related_name='settings', on_delete=models.CASCADE)
    profile = models.ForeignKey(SettingsProfile)
    avatar = models.ForeignKey(SettingsAvatar)


class Rank(models.Model):
    user = models.OneToOneField(User, related_name='rank', on_delete=models.CASCADE)
    points = models.PositiveIntegerField(default=0)

    def up(self):
        self.points += 1
        self.save()

    def down(self):
        self.points -= 1
        self.save()

    def rank_pos(self):
        aggregate = Rank.objects.filter(points__gt=self.points).aggregate(ranking=Count('points'))
        return aggregate['ranking'] + 1


@receiver(post_save, sender=User)
def create_user_settings(sender, instance, created, **kwargs):
    if created and instance.username != 'AnonymousUser':
        settings_profile = SettingsProfile.objects.create()
        settings_avatar = SettingsAvatar.objects.create()
        settings = Settings.objects.create(user=instance, profile=settings_profile, avatar=settings_avatar)
        rank = Rank.objects.create(user=instance)
        notifications = NotificationModel.objects.create(user=instance)
        observers = FollowersUserModel.objects.create(user=instance)
        assign_perm('profile_account.change_settings', instance, settings)

@receiver(post_save, sender=User)
def save_user_settings(sender, instance, **kwargs):
    if instance.username != 'AnonymousUser':
        instance.settings.save()