# -*- coding: utf-8 -*-
import django_tables2 as tables
from django import forms
from django.utils.html import format_html
from django.core.urlresolvers import reverse_lazy, reverse
from .models import Notification
from eureka.models import Eureka
from concept.models import Concept
from comments.models import Comment

class NotificationsTable(tables.Table):
    type = tables.Column(verbose_name='Rodzaj', orderable=False, empty_values=())
    action = tables.Column(verbose_name='', orderable=False, empty_values=())

    def render_type(self, record):
        if record.content_type.app_label == 'comments':
            return 'Komentarz'
        elif record.content_type.app_label == 'eureka':
            return 'Eureka'
        elif record.content_type.app_label == 'concept':
            return 'Koncepcja'
        return record.content_type.app_label

    def render_action(self, record):
        seeed_first = ''
        if record.seeed_first and not record.seeed_second:
            seeed_first = 'link-tab-active'

        if isinstance(record.content_object, Eureka):
            return format_html('<a href="{}" class="link-tab {}"><i class="fa fa-external-link" aria-hidden="true"></i></a>', reverse('eureka:eureka_detail', kwargs={'slug': record.content_object.slug}), seeed_first)
        elif isinstance(record.content_object, Concept):
            return format_html('<a href="{}" class="link-tab {}"><i class="fa fa-external-link" aria-hidden="true"></i></a>', reverse('concept:concept_detail', kwargs={'slug': record.content_object.slug}), seeed_first)
        elif isinstance(record.content_object, Comment):
            eureka = Eureka.objects.filter(comments__in=[record.object_id])
            concept = Concept.objects.filter(comments__in=[record.object_id])
            if eureka:
                eureka = eureka[0]
                return format_html('<a href="{}{}{}" class="link-tab {}"><i class="fa fa-external-link" aria-hidden="true"></i></a>', reverse('eureka:eureka_detail', kwargs={'slug': eureka.slug}), '#', record.content_object.slug, seeed_first)
            elif concept:
                concept = concept[0]
                return format_html('<a href="{}{}{}" class="link-tab {}"><i class="fa fa-external-link" aria-hidden="true"></i></a>', reverse('concept:concept_detail', kwargs={'slug': concept.slug}), '#', record.content_object.slug, seeed_first)

        return ''

    class Meta:
        model = Notification
        fields = ['content', 'created', 'type', 'action']
