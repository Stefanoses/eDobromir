from django import template
from django.template.loader import render_to_string
from moderation.forms import ReportModerationForm
from notification.models import NotificationModel, Conversation

register = template.Library()


@register.simple_tag(takes_context=True)
def get_seeed_first_notification_count(context):
    request = context['request']
    notification_model = NotificationModel.objects.get(user=request.user)
    notification_count = notification_model.container.filter(seeed_first=False).count()
    return notification_count


@register.simple_tag(takes_context=True)
def get_seeed_first_conversation_count(context):
    request = context['request']
    conversation_count = Conversation.objects.filter(owners__in=[request.user]).exclude(seeed__in=[request.user]).count()
    return conversation_count


@register.inclusion_tag('notification_followers.html', takes_context=True)
def render_notification_followers(context, user):
    request = context['request']
    was_observer = False
    if user.observers.container.filter(id=request.user.id).exists():
        was_observer = True
    return {'request': request, 'was_observer': was_observer, 'object': user}


@register.inclusion_tag('notification_follow_tag.html', takes_context=True)
def render_notification_followers_tag(context, tag):
    request = context['request']
    was_observer = False
    if tag.observers.filter(id=request.user.id).exists():
        was_observer = True
    observers_count = tag.observers.count()
    return {'request': request, 'was_observer': was_observer, 'object': tag, 'observers_count': observers_count}


@register.inclusion_tag('notification_follow_sympathizer.html', takes_context=True)
def render_notification_followers_sympathizer(context, sympathizer):
    request = context['request']
    was_observer = False
    if sympathizer.observers.filter(id=request.user.id).exists():
        was_observer = True
    observers_count = sympathizer.observers.count()
    return {'request': request, 'was_observer': was_observer, 'object': sympathizer, 'observers_count': observers_count}