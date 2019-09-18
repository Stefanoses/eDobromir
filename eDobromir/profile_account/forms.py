# -*- coding: utf-8 -*-
from django import forms
from django.utils.translation import pgettext, ugettext, ugettext_lazy as _
from django.contrib.auth import get_user_model


class SignupForm(forms.Form):
    username = forms.CharField(max_length=10, label='Username')

    class Meta:
        model = get_user_model()
        fields = ['username']

    def signup(self, request, user):
        user.username = self.cleaned_data['username']
        user.save()

    def clean(self):
        form_data = self.cleaned_data
        if form_data.has_key('username'):
            if len(form_data['username']) > 15:
                self.add_error('username', 'Nazwa użytkownika może mieć maksymalnie 15 znaków.')
        return form_data