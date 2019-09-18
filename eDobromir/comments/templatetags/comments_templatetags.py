from django import template
from django.template.loader import render_to_string
from comments.forms import CommentCreateForm, CommentReplyForm
from comments.models import Comment

register = template.Library()


@register.inclusion_tag('comments_preview_less.html', takes_context=True)
def render_comments_preview_less(context, comment_object, node):
    return {'request': context['request'], 'comment_object': comment_object, 'node': node}


@register.inclusion_tag('comments_preview_more_eureka.html', takes_context=True)
def render_comments_preview_more_eureka(context, comment_object, node):
    return {'request': context['request'], 'comment_object': comment_object, 'node': node}


@register.inclusion_tag('comments_preview_more_concept.html', takes_context=True)
def render_comments_preview_more_concept(context, comment_object, node):
    return {'request': context['request'], 'comment_object': comment_object, 'node': node}


@register.inclusion_tag('comments_create.html', takes_context=True)
def render_comments_create(context):
    return {'request': context['request'], 'form': CommentCreateForm(auto_id='id_comment_%s')}


@register.inclusion_tag('comments_reply.html', takes_context=True)
def render_comments_reply(context):
    return {'request': context['request'], 'form': CommentReplyForm(auto_id='id_reply_%s')}


@register.inclusion_tag('comments_tree_eureka.html', takes_context=True)
def render_comments_tree_eureka(context, comment_object):
    return {'request': context['request'], 'comment_object': comment_object}


@register.inclusion_tag('comments_tree_concept.html', takes_context=True)
def render_comments_tree_concept(context, comment_object):
    return {'request': context['request'], 'comment_object': comment_object}


@register.inclusion_tag('comments_list.html', takes_context=True)
def render_popular_comments_list(context, comment_object, value):
    comments_list = comment_object.comments.filter(level=0, mask__is_delete=False).order_by('-num_vote_up')[:value]
    return {'request': context['request'], 'comment_object': comment_object, 'comments_list': comments_list}