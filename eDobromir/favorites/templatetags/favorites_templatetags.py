from django import template
from eureka.models import Eureka
from django.contrib.contenttypes.models import ContentType


register = template.Library()


@register.inclusion_tag('favorites_manage_eureka.html', takes_context=True)
def render_favorites_manager_eureka(context, favorite_content):
    request = context['request']
    was_favorite = favorite_content.favorites.filter(id=request.user.id).exists()
    return {'favorite_content': favorite_content, 'was_favorite': was_favorite, 'request': request}


@register.inclusion_tag('favorites_manage_concept.html', takes_context=True)
def render_favorites_manager_concept(context, favorite_content):
    request = context['request']
    was_favorite = favorite_content.favorites.filter(id=request.user.id).exists()
    return {'favorite_content': favorite_content, 'was_favorite': was_favorite, 'request': request}