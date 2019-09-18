# -*- coding: utf-8 -*-

from django.shortcuts import render
from django.views.generic.edit import UpdateView
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from models import SettingsProfile, SettingsAvatar
from django.contrib.auth.models import User
from guardian.mixins import PermissionRequiredMixin, UserObjectPermission
from allauth.account.views import *
from django.contrib import messages
from tables import RankTable
from django_tables2 import RequestConfig
from eureka.models import Eureka
from concept.models import Concept
from comments.models import Comment
from tags.models import DefaultTag
from allauth.socialaccount.views import ConnectionsView
from notification.models import FollowersUserModel
from .tables import *
from django.contrib.auth.mixins import UserPassesTestMixin
from tags.models import Sympathizer, DefaultTag


class LoginSignupView(TemplateView):
    template_name = 'account_login_signup.html'

    def get_context_data(self, **kwargs):
        context = super(LoginSignupView, self).get_context_data(**kwargs)
        context['login_form'] = LoginForm()
        context['signup_form'] = SignupForm()
        context['active_page'] = 'login_signup'
        return context


class ProfileDetail(DetailView):
    model = User
    template_name = 'profile_detail.html'
    context_object_name = 'user_profile'

    def get_object(self, queryset=None):
        return User.objects.get(username=self.kwargs['username'])

    def get_context_data(self, **kwargs):
        context = super(ProfileDetail, self).get_context_data(**kwargs)
        context['eureka_actions'] = Eureka.objects.filter(created_by=self.object, is_published=True).count()
        context['concept_actions'] = Concept.objects.filter(created_by=self.object).count()
        context['observe_actions'] = self.object.observers.container.count()
        context['owner_sympathizers'] = Sympathizer.objects.filter(created_by=self.object)
        context['observer_sympathizers'] = Sympathizer.objects.filter(observers__in=[self.object])
        context['observer_tags'] = DefaultTag.objects.filter(observers__in=[self.object])
        return context


class ProfileActivityEurekaSketchView(LoginRequiredMixin, UserPassesTestMixin, ProfileDetail):
    template_name = 'profile_detail_activity_eureka.html'

    def get_permission_object(self):
        return self.request.user

    def test_func(self):
        return self.request.user == self.get_object()

    def get_context_data(self, **kwargs):
        context = super(ProfileActivityEurekaSketchView, self).get_context_data(**kwargs)
        table = ActivityEurekaTable(Eureka.objects.filter(created_by=self.object, is_published=False), order_by='-published')
        RequestConfig(self.request, paginate={'per_page': 30}).configure(table)
        context['active_activity'] = 'eureka'
        context['active_tab'] = 'sketch'
        context['table'] = table
        return context


class ProfileActivityEurekaView(ProfileDetail):
    template_name = 'profile_detail_activity_eureka.html'

    def get_context_data(self, **kwargs):
        context = super(ProfileActivityEurekaView, self).get_context_data(**kwargs)
        table = ActivityEurekaTable(Eureka.objects.filter(created_by=self.object, is_waiting=False, is_published=True), order_by='-published')
        RequestConfig(self.request, paginate={'per_page': 30}).configure(table)
        context['active_activity'] = 'eureka'
        context['active_tab'] = 'main'
        context['table'] = table
        return context


class ProfileActivityEurekaWaitingView(ProfileDetail):
    template_name = 'profile_detail_activity_eureka.html'

    def get_context_data(self, **kwargs):
        context = super(ProfileActivityEurekaWaitingView, self).get_context_data(**kwargs)
        table = ActivityEurekaTable(Eureka.objects.filter(created_by=self.object, is_waiting=True, is_published=True), order_by='-published')
        RequestConfig(self.request, paginate={'per_page': 30}).configure(table)
        context['active_activity'] = 'eureka'
        context['active_tab'] = 'waiting'
        context['table'] = table
        return context


class ProfileActivityEurekaVoteView(ProfileDetail):
    template_name = 'profile_detail_activity_eureka.html'

    def get_context_data(self, **kwargs):
        context = super(ProfileActivityEurekaVoteView, self).get_context_data(**kwargs)
        table = ActivityEurekaTable(Eureka.votes.all(self.object.id), order_by='-published')
        RequestConfig(self.request, paginate={'per_page': 30}).configure(table)
        context['active_activity'] = 'eureka'
        context['active_tab'] = 'vote'
        context['table'] = table
        return context


class ProfileActivityEurekaFavoriteView(ProfileDetail):
    template_name = 'profile_detail_activity_eureka.html'

    def get_context_data(self, **kwargs):
        context = super(ProfileActivityEurekaFavoriteView, self).get_context_data(**kwargs)
        table = ActivityEurekaTable(Eureka.objects.filter(favorites__in=[self.object.id]), order_by='-published')
        RequestConfig(self.request, paginate={'per_page': 30}).configure(table)
        context['active_activity'] = 'eureka'
        context['active_tab'] = 'favorite'
        context['table'] = table
        return context


class ProfileActivityConceptView(ProfileDetail):
    template_name = 'profile_detail_activity_concept.html'

    def get_context_data(self, **kwargs):
        context = super(ProfileActivityConceptView, self).get_context_data(**kwargs)
        table = ActivityConceptTable(Concept.objects.filter(created_by=self.object), order_by='-published')
        RequestConfig(self.request, paginate={'per_page': 30}).configure(table)
        context['active_activity'] = 'concept'
        context['active_tab'] = 'concept'
        context['table'] = table
        return context


class ProfileActivityConceptVoteView(ProfileDetail):
    template_name = 'profile_detail_activity_concept.html'

    def get_context_data(self, **kwargs):
        context = super(ProfileActivityConceptVoteView, self).get_context_data(**kwargs)
        table = ActivityConceptTable(Concept.votes.all(self.object.id), order_by='-published')
        RequestConfig(self.request, paginate={'per_page': 30}).configure(table)
        context['active_activity'] = 'concept'
        context['active_tab'] = 'vote'
        context['table'] = table
        return context


class ProfileActivityConceptFavoriteView(ProfileDetail):
    template_name = 'profile_detail_activity_concept.html'

    def get_context_data(self, **kwargs):
        context = super(ProfileActivityConceptFavoriteView, self).get_context_data(**kwargs)
        table = ActivityConceptTable(Concept.objects.filter(favorites__in=[self.object.id]), order_by='-published')
        RequestConfig(self.request, paginate={'per_page': 30}).configure(table)
        context['active_activity'] = 'concept'
        context['active_tab'] = 'favorite'
        context['table'] = table
        return context


class ProfileActivityObservers(ProfileDetail):
    template_name = 'profile_detail_activity_observers.html'

    def get_context_data(self, **kwargs):
        context = super(ProfileActivityObservers, self).get_context_data(**kwargs)
        observedUserModel = FollowersUserModel.objects.filter(container__in=[self.object.id])
        table = ActivityUserTable(User.objects.filter(observers__in=observedUserModel), order_by='-published')
        RequestConfig(self.request, paginate={'per_page': 30}).configure(table)
        context['active_activity'] = 'notification'
        context['active_tab'] = 'observers'
        context['table'] = table
        return context


class ProfileActivityFollowers(ProfileDetail):
    template_name = 'profile_detail_activity_observers.html'

    def get_context_data(self, **kwargs):
        context = super(ProfileActivityFollowers, self).get_context_data(**kwargs)
        table = ActivityUserTable(self.object.observers.container.all(), order_by='-published')
        RequestConfig(self.request, paginate={'per_page': 30}).configure(table)
        context['active_activity'] = 'notification'
        context['active_tab'] = 'followers'
        context['table'] = table
        return context


class SettingsProfileView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = SettingsProfile
    template_name = 'profile_settings_profile.html'
    fields = ['name', 'last_name', 'public_email', 'website', 'town',
              'social_facebook', 'social_twitter', 'social_google_plus', 'social_linkedin', 'social_youtube',
              'description']
    permission_required = 'profile_account.change_settings'
    raise_exception = True

    def get_object(self, queryset=None):
        return self.request.user.settings.profile

    def get_permission_object(self):
        return self.request.user.settings

    def get_success_url(self):
        messages.success(self.request, 'Profil zaktualizowany pomyślnie.')
        return reverse_lazy('account_settings_profile')

    def get_context_data(self, **kwargs):
        context = super(SettingsProfileView, self).get_context_data(**kwargs)
        context['active_page'] = 'settings_profile'
        context['user_profile'] = self.request.user
        context['owner_sympathizers'] = Sympathizer.objects.filter(created_by=self.request.user)
        context['observer_sympathizers'] = Sympathizer.objects.filter(observers__in=[self.request.user])
        context['observer_tags'] = DefaultTag.objects.filter(observers__in=[self.request.user])
        return context


class SettingsPasswordUpdateView(LoginRequiredMixin, PasswordChangeView):
    def get_context_data(self, **kwargs):
        context = super(SettingsPasswordUpdateView, self).get_context_data(**kwargs)
        context['active_page'] = 'settings_password'
        context['user_profile'] = self.request.user
        context['owner_sympathizers'] = Sympathizer.objects.filter(created_by=self.request.user)
        context['observer_sympathizers'] = Sympathizer.objects.filter(observers__in=[self.request.user])
        context['observer_tags'] = DefaultTag.objects.filter(observers__in=[self.request.user])
        return context


class SettingsEmailUpdateView(LoginRequiredMixin, EmailView):
    def get_context_data(self, **kwargs):
        context = super(SettingsEmailUpdateView, self).get_context_data(**kwargs)
        context['active_page'] = 'settings_email'
        context['user_profile'] = self.request.user
        context['owner_sympathizers'] = Sympathizer.objects.filter(created_by=self.request.user)
        context['observer_sympathizers'] = Sympathizer.objects.filter(observers__in=[self.request.user])
        context['observer_tags'] = DefaultTag.objects.filter(observers__in=[self.request.user])
        return context


class SettingsAvatarView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = SettingsAvatar
    template_name = 'profile_settings_avatar.html'
    fields = ['avatar_image']
    permission_required = 'profile_account.change_settings'
    raise_exception = True

    def get_object(self, queryset=None):
        return self.request.user.settings.avatar

    def get_permission_object(self):
        return self.request.user.settings

    def get_success_url(self):
        messages.success(self.request, 'Avatar zaktualizowany pomyślnie.')
        return reverse_lazy('account_settings_avatar')

    def get_context_data(self, **kwargs):
        context = super(SettingsAvatarView, self).get_context_data(**kwargs)
        context['active_page'] = 'settings_avatar'
        context['user_profile'] = self.request.user
        return context


class SettingsSocialUpdateView(LoginRequiredMixin, ConnectionsView):
    def get_context_data(self, **kwargs):
        context = super(SettingsSocialUpdateView, self).get_context_data(**kwargs)
        context['active_page'] = 'settings_social'
        context['user_profile'] = self.request.user
        return context


class RankListView(ListView):
    model = User
    template_name = 'profile_user_rank.html'

    def get_queryset(self):
        queryset = super(RankListView, self).get_queryset()
        queryset = queryset.filter(is_active=True).exclude(username='AnonymousUser')
        return queryset

    def get_context_data(self, **kwargs):
        table = RankTable(self.get_queryset(), order_by='-position')
        RequestConfig(self.request, paginate={'per_page': 30}).configure(table)
        contex = super(RankListView, self).get_context_data(**kwargs)
        contex['active_page'] = 'rank'
        contex['table'] = table
        return contex





