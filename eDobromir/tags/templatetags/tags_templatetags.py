from django import template
from django.template.loader import render_to_string
from taggit.models import Tag
from annoying.functions import get_object_or_None
from tags.models import DefaultTag, Sympathizer
from django.db.models import Count


register = template.Library()


@register.inclusion_tag('tags_most_popular.html', takes_context=True)
def render_tags_most_popular(context, value):
    tags = DefaultTag.objects.annotate(observers_count=Count('observers')).order_by('-observers_count')[:value]
    return {'request': context['request'], 'tags': tags}


@register.inclusion_tag('tags_preview_less.html', takes_context=True)
def render_tag_preview_less(context, tag_name):
    tag = get_object_or_None(DefaultTag, name=tag_name)
    return {'request': context['request'], 'tag': tag, 'tag_name': tag_name}


@register.inclusion_tag('tags_preview_more.html', takes_context=True)
def render_tag_preview_more(context, tag_name):
    tag = get_object_or_None(DefaultTag, name=tag_name)
    return {'request': context['request'], 'tag':tag, 'tag_name':tag_name}


@register.inclusion_tag('sympathizer_most_popular.html', takes_context=True)
def render_sympathizer_most_popular(context, value):
    sympathizers = Sympathizer.objects.annotate(observers_count=Count('observers')).order_by('-observers_count')[:value]
    return {'request': context['request'], 'sympathizers': sympathizers}


@register.inclusion_tag('sympathizer_preview_less.html', takes_context=True)
def render_sympathizer_preview_less(context, sympathizer_name):
    sympathizer = get_object_or_None(Sympathizer, name=sympathizer_name)
    return {'request': context['request'], 'sympathizer': sympathizer, 'sympathizer_name': sympathizer_name}


@register.inclusion_tag('sympathizer_preview_more.html', takes_context=True)
def render_sympathizer_preview_more(context, sympathizer_name):
    sympathizer = get_object_or_None(Sympathizer, name=sympathizer_name)
    return {'request': context['request'], 'sympathizer': sympathizer, 'sympathizer_name': sympathizer_name}