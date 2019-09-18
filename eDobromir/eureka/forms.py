# -*- coding: utf-8 -*-

from .models import Eureka
from django import forms
from fontawesome.utils import get_icon_choices
from django.contrib import messages
from tags.models import Sympathizer
import urllib
from BeautifulSoup import BeautifulSoup
import json
import os
from django.conf import settings
from django.template.defaultfilters import slugify


# CHOICES = Sympathizer.objects.all().values_list('id', 'name') or None
#
#
# class SympathizerEurekaIconWidget(forms.Select):
#     def create_option(self, name, value, label, selected, index, subindex=None, attrs=None):
#         option = super(SympathizerEurekaIconWidget, self).create_option(name, value, label, selected, index, subindex=None, attrs=None)
#         option['attrs'] = {'data-icon': Sympathizer.objects.get(id=value).icon}
#         return option


class EurekaCreateForm(forms.ModelForm):
    # sympathizers = forms.IntegerField(widget=SympathizerEurekaIconWidget(choices=CHOICES), required=False, label='Sympatycy')
    #
    # def clean_sympathizers(self):
    #     data = self.cleaned_data['sympathizers']
    #     data = Sympathizer.objects.get(id=data)
    #     return data
    preview_image = forms.ImageField(required=False, label='Miniaturka (nie wymagana, jeśli dodany jest link doda się automatycznie)')

    def clean_preview_image(self):
        data = self.cleaned_data['preview_image']
        link = self.cleaned_data['link']
        embed_link = 'https://www.iframe.ly/api/oembed?url=' + link + '&api_key=c3e45645472c7d510319ab'
        if data:
            return data
        elif link:
            content = urllib.urlopen(embed_link).read()
            json_data = json.loads(content)
            file_link = json_data['thumbnail_url']

            if not file_link:
                return 'preview_images/default-no-image.png'
            else:
                link_name = link.split('/')[-1]
                file_name = file_link.split('/')[-1]
                final_file_name = slugify(link_name.replace('/', '') + file_name.replace('/', '')) + '.' + file_name.split('.')[-1]
                urllib.urlretrieve(file_link, os.path.join(settings.MEDIA_ROOT + '/preview_images/', os.path.basename(final_file_name)))
                return 'preview_images/' + final_file_name
        else:
            return 'preview_images/default-no-image.png'

    class Meta:
        model = Eureka
        fields = ['title', 'tags', 'sympathizers', 'description', 'link', 'content_type', 'preview_image', 'difficult', 'price']
