# -*- coding: utf-8 -*-
from django import forms
from .models import ErrorReport


class ErrorReportForm(forms.ModelForm):
    error_image = forms.FileField(required=False, label='Zdjęcie (niewymagane)')

    class Meta:
        model = ErrorReport
        fields = ['contact_email', 'error_code', 'error_login_state', 'error_type', 'error_link', 'error_description', 'error_image']


class ContactForm(forms.Form):
    name = forms.CharField(required=True, label='Imię', max_length=20)
    email = forms.EmailField(required=True, label='E-mail', max_length=30)
    message = forms.CharField(widget=forms.Textarea, max_length=1000, label='Wiadomość', required=True)