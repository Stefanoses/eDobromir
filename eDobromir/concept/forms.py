# -*- coding: utf-8 -*-
from django import forms
from .models import Concept
from fontawesome.fields import IconField
from fontawesome.forms import IconFormField, IconWidget
from django.forms import ValidationError
from fontawesome.utils import get_icon_choices
from django.contrib import messages
from tags.models import Sympathizer


# class SympathizerIconWidget(forms.Select):
#     def __init__(self, attrs=None):
#         super(SympathizerIconWidget, self).__init__(attrs, choices=Sympathizer.objects.all().values_list('id', 'name'))
#
#     def create_option(self, name, value, label, selected, index, subindex=None, attrs=None):
#         option = super(SympathizerIconWidget, self).create_option(name, value, label, selected, index, subindex=None, attrs=None)
#         option['attrs'] = {'data-icon': Sympathizer.objects.get(id=value).icon}
#         return option
#

class ConceptCreateForm(forms.ModelForm):
    # sympathizers = forms.IntegerField(widget=SympathizerIconWidget(), required=False, label='Sympatycy')
    #
    # def clean_sympathizers(self):
    #     data = self.cleaned_data['sympathizers']
    #     if data:
    #         data = Sympathizer.objects.get(id=data)
    #     return data

    class Meta:
        model = Concept
        fields = ['content', 'sympathizers', 'tags']
