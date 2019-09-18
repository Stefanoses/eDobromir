from django.conf.urls import url, include
from django.contrib import admin
from .views import *


urlpatterns = [
    url(r'^eureka/(?P<slug>[-\w]+)/report/$', ModerationReportEurekaView.as_view(), name='moderation_report_eureka'),
    url(r'^eureka/(?P<slug>[-\w]+)/comments/(?P<comment_slug>[-\w]+)/report/$', ModerationReportEurekaCommentView.as_view(), name='moderation_report_eureka_comment'),
    # url(r'^eureka/(?P<slug>[-\w]+)/links/(?P<slug>[-\w]+)/report/$', ModerationReportView.as_view(), name='eureka_instruction_detail'),
    #
    url(r'^concept/(?P<slug>[-\w]+)/report/$', ModerationReportConceptView.as_view(), name='moderation_report_concept'),
    url(r'^concept/(?P<slug>[-\w]+)/comments/(?P<comment_slug>[-\w]+)/report/$', ModerationReportConceptCommentView.as_view(), name='moderation_report_concept_comment'),
    # url(r'^concept/(?P<slug>[-\w]+)/links/(?P<slug>[-\w]+)/report/$', ModerationReportView.as_view(), name='eureka_instruction_detail'),
    #
    # url(r'^account/user/(?P<slug>[-\w]+)/report/$', ModerationReportView.as_view(), name='eureka_instruction_detail'),
]
