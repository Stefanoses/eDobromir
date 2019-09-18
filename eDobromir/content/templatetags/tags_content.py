from django import template
from django.template.loader import render_to_string
from concept.models import Concept
from content.forms import ErrorReportForm
from guardian.decorators import permission_required
from django.contrib.auth.decorators import login_required


register = template.Library()


@register.inclusion_tag('content_error_report_create.html', takes_context=True)
def render_content_error_report(context):
    return {'form': ErrorReportForm(), 'request': context['request']}


@register.inclusion_tag('content_error_report_moderation_actions.html', takes_context=True)
def render_content_error_moderation_actions(context, error):
    has_perm = context['request'].user.has_perm('content.delete_errorreport') and context['request'].user.has_perm('content.change_errorreport')
    return {'has_perm': has_perm, 'error': error, 'request': context['request']}