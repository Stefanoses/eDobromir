from django.conf.urls import url, include
from django.contrib import admin
from .views import *


urlpatterns = [
    url(r'^eureka/(?P<slug>[-\w]+)/linked/create/$', LinkedEurekaCreateView.as_view(), name='linked_eureka_create'),
    url(r'^concept/(?P<slug>[-\w]+)/linked/create/$', LinkedConceptCreateView.as_view(), name='linked_concept_create'),
]
