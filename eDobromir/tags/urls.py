from django.conf.urls import url, include
from django.contrib import admin
from .views import *


urlpatterns = [
    url(r'^tag/list/$', TagListView.as_view(), name='tag_list'),
    url(r'^sympathizer/list/$', SympathizerListView.as_view(), name='sympathizer_list'),
    url(r'^sympathizer/create/$', SympathizerCreateView.as_view(), name='sympathizer_create'),
]
