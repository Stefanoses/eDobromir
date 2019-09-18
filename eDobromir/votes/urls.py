from django.conf.urls import url, include
from django.contrib import admin
from .views import *


urlpatterns = [
    url(r'^eureka/(?P<slug>[-\w]+)/votes/$', VoteDetailEurekaView.as_view(), name='vote_detail_eureka'),
    url(r'^eureka/(?P<slug>[-\w]+)/votes/up/$', VoteUpEurekaView.as_view(), name='vote_up_eureka'),
    url(r'^eureka/(?P<slug>[-\w]+)/votes/delete/$', VoteDownEurekaView.as_view(), name='vote_down_eureka'),

    url(r'^eureka/(?P<slug>[-\w]+)/comments/(?P<comment_slug>[-\w]+)/votes/up/$', VoteUpEurekaCommentView.as_view(), name='vote_up_eureka_comment'),
    url(r'^eureka/(?P<slug>[-\w]+)/comments/(?P<comment_slug>[-\w]+)/votes/delete/$', VoteDownEurekaCommentView.as_view(), name='vote_down_eureka_comment'),

    url(r'^eureka/(?P<slug>[-\w]+)/links/(?P<linked_slug>[-\w]+)/votes/up/$', VoteUpEurekaLinkedView.as_view(), name='vote_up_eureka_linked'),
    url(r'^eureka/(?P<slug>[-\w]+)/links/(?P<linked_slug>[-\w]+)/votes/delete/$', VoteDownEurekaLinkedView.as_view(), name='vote_down_eureka_linked'),

    url(r'^concept/(?P<slug>[-\w]+)/votes/$', VoteDetailConceptView.as_view(), name='vote_detail_concept'),
    url(r'^concept/(?P<slug>[-\w]+)/votes/up/$', VoteUpConceptView.as_view(), name='vote_up_concept'),
    url(r'^concept/(?P<slug>[-\w]+)/votes/delete/$', VoteDownConceptView.as_view(), name='vote_down_concept'),

    url(r'^concept/(?P<slug>[-\w]+)/comments/(?P<comment_slug>[-\w]+)/votes/up/$', VoteUpConceptCommentView.as_view(), name='vote_up_concept_comment'),
    url(r'^concept/(?P<slug>[-\w]+)/comments/(?P<comment_slug>[-\w]+)/votes/delete/$', VoteDownConceptCommentView.as_view(), name='vote_down_concept_comment'),

    url(r'^concept/(?P<slug>[-\w]+)/links/(?P<linked_slug>[-\w]+)/votes/up/$', VoteUpConceptLinkedView.as_view(), name='vote_up_concept_linked'),
    url(r'^concept/(?P<slug>[-\w]+)/links/(?P<linked_slug>[-\w]+)/votes/delete/$', VoteDownConceptLinkedView.as_view(), name='vote_down_concept_linked'),

]
