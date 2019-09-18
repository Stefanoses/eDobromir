from django.conf.urls import url, include
from django.contrib import admin
from .views import *


urlpatterns = [
    url(r'^eureka/(?P<slug>[-\w]+)/comments/create/$', CommentEurekaCreateView.as_view(), name='comment_eureka_create'),
    url(r'^eureka/(?P<slug>[-\w]+)/comments/(?P<comment_slug>[-\w]+)/reply/$', CommentEurekaReplyView.as_view(), name='comment_eureka_reply'),
    url(r'^eureka/(?P<slug>[-\w]+)/comments/(?P<comment_slug>[-\w]+)/delete/$', CommentEurekaDeleteView.as_view(), name='comment_eureka_delete'),

    url(r'^concept/(?P<slug>[-\w]+)/comments/create/$', CommentConceptCreateView.as_view(), name='comment_concept_create'),
    url(r'^concept/(?P<slug>[-\w]+)/comments/(?P<comment_slug>[-\w]+)/reply/$', CommentConceptReplyView.as_view(), name='comment_concept_reply'),
    url(r'^concept/(?P<slug>[-\w]+)/comments/(?P<comment_slug>[-\w]+)/delete/$', CommentConceptDeleteView.as_view(), name='comment_concept_delete'),
]
