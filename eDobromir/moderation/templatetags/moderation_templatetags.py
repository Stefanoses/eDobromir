from django import template
from django.template.loader import render_to_string
from moderation.forms import ReportModerationForm


register = template.Library()


def is_reported(request, report_object):
    if request.user.is_authenticated():
        return report_object.moderations.filter(created_by=request.user.id).exists()
    return False


@register.inclusion_tag('moderation_report_eureka_create.html', takes_context=True)
def render_moderation_report_eureka_create(context, report_object):
    request = context['request']
    return {'request': request, 'reportObject': report_object, 'was_report': is_reported(request, report_object)}


@register.inclusion_tag('moderation_report_modal.html', takes_context=True)
def render_moderation_report_modal(context):
    request = context['request']
    return {'request': request, 'form': ReportModerationForm()}


@register.inclusion_tag('moderation_report_concept_create.html', takes_context=True)
def render_moderation_report_concept_create(context, report_object):
    request = context['request']
    return {'request': request, 'reportObject': report_object,
            'form': ReportModerationForm(), 'was_report': is_reported(request, report_object)}


@register.inclusion_tag('moderation_report_eureka_comment_create.html', takes_context=True)
def render_moderation_report_eureka_comment_create(context, eureka, report_object):
    request = context['request']
    return {'request': request, 'eureka': eureka, 'reportObject': report_object,
            'form': ReportModerationForm(), 'was_report': is_reported(request, report_object)}


@register.inclusion_tag('moderation_report_concept_comment_create.html', takes_context=True)
def render_moderation_report_concept_comment_create(context, concept, report_object):
    request = context['request']
    return {'request': request, 'concept': concept, 'reportObject': report_object,
            'form': ReportModerationForm(), 'was_report': is_reported(request, report_object)}


@register.inclusion_tag('moderation_report_detail.html', takes_context=True)
def render_moderation_report_detail(context, report_object):
    return {'request': context['request'], 'reportObject': report_object}