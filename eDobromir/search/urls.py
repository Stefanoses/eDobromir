from django.conf.urls import url
from django.contrib import admin
from .views import *

urlpatterns = [
    url(r'^$', SearchEurekaView.as_view(), name='search_eureka'),
    url(r'^waiting/$', SearchEurekaWaitingView.as_view(), name='search_eureka_waiting'),
    url(r'^concepts/$', SearchConceptView.as_view(), name='search_concept'),

    url(r'^search/eureka/$', SearchMixedEurekaView.as_view(), name='search_mixed_eureka'),
    url(r'^search/waiting/$', SearchMixedEurekaWaitingView.as_view(), name='search_mixed_eureka_waiting'),
    url(r'^search/concept/$', SearchMixedConceptView.as_view(), name='search_mixed_concept'),
    url(r'^search/everywhere/$', SearchMixedEverywhereView.as_view(), name='search_mixed_everywhere'),
]
