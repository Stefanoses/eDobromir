# -*- coding: utf-8 -*-
import django_tables2 as tables
from .models import ErrorReport
from django import forms
from django.utils.html import format_html
from django.core.urlresolvers import reverse_lazy, reverse

class ErrorReportTable(tables.Table):
    modified = tables.Column(verbose_name='Zaktualizowano')
    action = tables.Column(verbose_name='', orderable=False, empty_values=())

    def render_action(self, record):
        return format_html('<a href="{}" class="link-tab">Więcej</a>', reverse('content:content_error_detail', kwargs={'pk': record.id}))

    class Meta:
        model = ErrorReport
        fields = ['id', 'modified', 'error_type', 'actual_state', 'action']
