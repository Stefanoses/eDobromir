# -*- coding: utf-8 -*-

from django import forms
from ckeditor.widgets import CKEditorWidget
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, ButtonHolder, Submit, Field

class SearchForm(forms.Form):
    search_input = forms.CharField(max_length=100, label='Co cię interesuje? @użytkownik, #tag', required=False)
