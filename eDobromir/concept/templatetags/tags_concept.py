from django import template
from django.template.loader import render_to_string
from concept.models import Concept


register = template.Library()


@register.inclusion_tag('concept_preview_big.html', takes_context=True)
def render_concept_preview_big(context, concept):
    return {'concept': concept, 'request': context['request']}


@register.inclusion_tag('concept_preview_big_extended.html', takes_context=True)
def render_concept_preview_big_extended(context, concept):
    return {'concept': concept, 'request': context['request']}


@register.inclusion_tag('concept_preview_medium_extended.html', takes_context=True)
def render_concept_preview_medium_extended(context, concept):
    return {'concept': concept, 'request': context['request']}


@register.inclusion_tag('concept_preview_small.html', takes_context=True)
def render_concept_preview_small(context, concept):
    return {'concept': concept, 'request': context['request']}


@register.inclusion_tag('concept_preview_small_list.html', takes_context=True)
def render_concept_preview_small_random_list(context, value):
    list = Concept.objects.all().order_by('?')[:value]
    return {'list': list, 'request': context['request']}


@register.inclusion_tag('concept_preview_small_list.html', takes_context=True)
def render_similar_concept(context, concept, value):
    list = Concept.objects.filter(tags__name__in=concept.tags.names()).exclude(pk=concept.pk)[:value]
    return {'list': list, 'request': context['request']}