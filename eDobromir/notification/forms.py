# -*- coding: utf-8 -*-
from django import forms
from .models import *
from django.contrib.auth.models import User
#
# class ConversationCreateForm(forms.ModelForm):
#     message = forms.CharField(max_length=1000, label='Wiadomość', widget=forms.Textarea)
#
#     class Meta:
#         model = Conversation
#         fields = ['recipient', 'message']
