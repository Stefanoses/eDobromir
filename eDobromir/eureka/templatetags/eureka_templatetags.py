from django import template
from eureka.models import Eureka
register = template.Library()


@register.inclusion_tag('eureka_preview_big.html', takes_context=True)
def render_eureka_preview_big(context, eureka):
    return {'eureka': eureka, 'request': context['request']}


@register.inclusion_tag('eureka_preview_big_link_to_instruction.html', takes_context=True)
def render_eureka_preview_big_link_to_instruction(context, eureka):
    return {'eureka': eureka, 'request': context['request']}


@register.inclusion_tag('eureka_preview_small.html', takes_context=True)
def render_eureka_preview_small(context, eureka):
    return {'eureka': eureka, 'request': context['request']}


@register.inclusion_tag('eureka_preview_small_list.html', takes_context=True)
def render_eureka_random_list(context, value):
    eureka_random_list = Eureka.objects.filter(is_waiting=False, is_published=True).order_by('?')[:value]
    return {'list': eureka_random_list, 'request': context['request']}


@register.inclusion_tag('eureka_preview_small_list.html', takes_context=True)
def render_eureka_waiting_random_list(context, value):
    eureka_waiting_random_list = Eureka.objects.filter(is_waiting=True, is_published=True).order_by('?')[:value]
    return {'list': eureka_waiting_random_list, 'request': context['request']}


@register.inclusion_tag('eureka_preview_small_list.html', takes_context=True)
def render_similar_eureka_list(context, eureka, value):
    similar_eureka_list = Eureka.objects.filter(tags__name__in=eureka.tags.names(), is_published=True).exclude(pk=eureka.pk).distinct()[:value]
    return {'list': similar_eureka_list, 'request':context['request']}
