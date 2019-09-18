from django import template
from django.shortcuts import render_to_response, HttpResponse, render
from django.template.loader import render_to_string

register = template.Library()


def is_voting(request, vote_object):
    if request.user.is_authenticated():
        return vote_object.votes.exists(request.user.id)
    else:
        return False


@register.inclusion_tag('vote_eureka.html', takes_context=True)
def render_vote_eureka(context, eureka):
    return {'request': context['request'], 'object': eureka, 'was_voting': is_voting(context['request'], eureka)}


@register.inclusion_tag('vote_eureka_comment.html', takes_context=True)
def render_vote_eureka_comment(context, eureka, comment):
    return {'request': context['request'], 'eureka': eureka, 'object': comment, 'was_voting': is_voting(context['request'], comment)}


@register.inclusion_tag('vote_eureka_linked.html', takes_context=True)
def render_vote_eureka_linked(context, eureka, linked):
    return {'request': context['request'], 'eureka': eureka, 'object': linked, 'was_voting': is_voting(context['request'], linked)}


@register.inclusion_tag('vote_concept_linked.html', takes_context=True)
def render_vote_concept_linked(context, concept, linked):
    return {'request': context['request'], 'concept': concept, 'object': linked, 'was_voting': is_voting(context['request'], linked)}


@register.inclusion_tag('vote_concept.html', takes_context=True)
def render_vote_concept(context, concept):
    return {'request': context['request'], 'object': concept, 'was_voting': is_voting(context['request'], concept)}


@register.inclusion_tag('vote_concept_comment.html', takes_context=True)
def render_vote_concept_comment(context, concept, comment):
    return {'request': context['request'], 'concept': concept, 'object': comment, 'was_voting': is_voting(context['request'], comment)}


@register.inclusion_tag('vote_detail.html')
def render_vote_detail(voteObject):
    return {'voteObject': voteObject}