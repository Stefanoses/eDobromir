from allauth.account.adapter import DefaultAccountAdapter
from django.contrib.auth.models import Group
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save
from guardian.shortcuts import assign_perm
from .models import SettingsProfile, Settings, SettingsAvatar


class UserAccountAdapter(DefaultAccountAdapter):
    def save_user(self, request, user, form, commit=True):
        user = super(UserAccountAdapter, self).save_user(request, user, form, False)
        user.save()
        users_group = Group.objects.get(name='users')
        user.groups.add(users_group)
