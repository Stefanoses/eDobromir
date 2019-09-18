from django import template
from django.shortcuts import render_to_response, HttpResponse, render
from django.template.loader import render_to_string
from eureka.models import Eureka
from concept.models import Concept
from django.contrib.auth.models import User
from django.db.models import Count
from django.db.models import Q


register = template.Library()


@register.inclusion_tag('profile_user_preview.html', takes_context=True)
def render_profile_preview(context, user):
    profile_position = user.rank.rank_pos()
    profile_eureka_count = Eureka.objects.filter(created_by=user, is_published=True).count()
    profile_concept_count = Concept.objects.filter(created_by=user).count()
    profile_observe_count = user.observers.container.count()
    return {'profile': user,
            'profile_position': profile_position,
            'profile_eureka_count': profile_eureka_count,
            'profile_concept_count': profile_concept_count,
            'profile_observe_count': profile_observe_count,
            'request': context['request']}


@register.inclusion_tag('profile_user_list.html', takes_context=True)
def render_profile_list(context, value):
    all_users_count = User.objects.all().count()
    profiles = User.objects.filter(~Q(email='')).order_by('-rank__points')[:value]
    return {'all_users_count': all_users_count, 'profiles': profiles, 'request': context['request']}


def get_user_properties(user):
    if isinstance(user, int):
        user = User.objects.get(pk=user)
    if isinstance(user, long):
        user = User.objects.get(pk=user)
    if isinstance(user, str):
        user = User.objects.get(username=user)
    username = user.username
    date_joined = user.date_joined
    rank_points = user.rank.points
    rank_position = user.rank.rank_pos()

    color = '#777777'
    if rank_points >= 10:
        color = '#337AB7'
    if rank_points >= 100:
        color = '#C7254E'

    return {'color': color, 'username': username, 'date_joined': date_joined, 'rank_position': rank_position}


@register.inclusion_tag('profile_username.html')
def render_profile_username(user):
    user_properties = get_user_properties(user)
    return {'username': user_properties['username'], 'color': user_properties['color']}


@register.inclusion_tag('profile_username_clean.html')
def render_profile_username_clean(user):
    user_properties = get_user_properties(user)
    return {'username': user_properties['username'], 'color': user_properties['color']}