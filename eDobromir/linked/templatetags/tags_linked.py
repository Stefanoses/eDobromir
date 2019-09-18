from django import template
from django.template.loader import render_to_string
from linked.forms import LinkedCreateForm


register = template.Library()


@register.inclusion_tag('linked_eureka_create.html', takes_context=True)
def render_linked_eureka_create(context, linked_object):
    return {'request': context['request'], 'linkedObject': linked_object, 'form': LinkedCreateForm()}


@register.inclusion_tag('linked_concept_create.html', takes_context=True)
def render_linked_concept_create(context, linked_object):
    return {'request': context['request'], 'linkedObject': linked_object, 'form': LinkedCreateForm()}


@register.inclusion_tag('linked_eureka_list.html', takes_context=True)
def render_linked_eureka_list(context, linked_object):
    return {'request': context['request'], 'linkedObject':linked_object}


@register.inclusion_tag('linked_concept_list.html', takes_context=True)
def render_linked_concept_list(context, linked_object):
    return {'request': context['request'], 'linkedObject': linked_object}