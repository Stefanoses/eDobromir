# -*- coding: utf-8 -*-
from django import forms
from .models import Sympathizer
from fontawesome.fields import IconField
from fontawesome.forms import IconFormField, IconWidget
from django.forms import ValidationError
from fontawesome.utils import get_icon_choices
from django.contrib import messages


class SympathizerIconWidget(forms.Select):
    def __init__(self, attrs=None):
        super(SympathizerIconWidget, self).__init__(attrs, choices=get_icon_choices())

    def create_option(self, name, value, label, selected, index, subindex=None, attrs=None):
        option = super(SympathizerIconWidget, self).create_option(name, value, label, selected, index, subindex=None, attrs=None)
        option['attrs'] = {'data-icon': option['value']}
        return option


class SympathizerCreateForm(forms.ModelForm):
    icon = IconFormField(widget=SympathizerIconWidget, required=False, label='Ikona')
    created_by = None

    def __init__(self, created_by, *args, **kwargs):
        self.created_by = created_by
        super(SympathizerCreateForm, self).__init__(*args, **kwargs)

    def clean_name(self):
        data = self.cleaned_data['name']
        if not data.islower():
            raise ValidationError('Nazwa może składać się wyłącznie z małych liter i musi posiadać przynajmniej jedną literę')
        return data

    def clean(self):
        if Sympathizer.objects.filter(created_by=self.created_by).count() >= 10:
            raise ValidationError('Nie możesz mieć więcej niż 10 tagów sympatyków')
        return super(SympathizerCreateForm, self).clean()

    class Meta:
        model = Sympathizer
        fields = ['name', 'icon']
