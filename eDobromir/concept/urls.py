from django.conf.urls import url, include
from django.contrib import admin
from .views import *


urlpatterns = [
    url(r'^concept/create/$', ConceptCreateView.as_view(), name='concept_create'),
    url(r'^concept/(?P<slug>[-\w]+)/$', ConceptDetailView.as_view(), name='concept_detail'),
    url(r'^concept/(?P<slug>[-\w]+)/delete/$', ConceptDeleteView.as_view(), name='concept_delete'),
]
