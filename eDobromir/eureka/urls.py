from django.conf.urls import url, include
from django.contrib import admin
from .views import *


urlpatterns = [
    url(r'^eureka/create/$', EurekaCreateView.as_view(), name='eureka_create'),
    url(r'^eureka/(?P<slug>[-\w]+)/update/$', EurekaUpdateView.as_view(), name='eureka_update'),
    url(r'^eureka/(?P<slug>[-\w]+)/delete/$', EurekaDeleteView.as_view(), name='eureka_delete'),
    url(r'^eureka/(?P<slug>[-\w]+)/$', EurekaDetailView.as_view(), name='eureka_detail'),
    url(r'^eureka/(?P<slug>[-\w]+)/summary/$', EurekaSummaryView.as_view(), name='eureka_summary'),

    url(r'^eureka/(?P<slug>[-\w]+)/instruction/$', EurekaInstructionDetailView.as_view(), name='eureka_instruction_detail'),
    url(r'^eureka/(?P<slug>[-\w]+)/instruction/step/create/', EurekaInstructionStepCreateView.as_view(), name='eureka_instruction_step_create'),
    url(r'^eureka/(?P<slug>[-\w]+)/instruction/step/(?P<step_slug>[-\w]+)/update/', EurekaInstructionStepUpdateView.as_view(), name='eureka_instruction_step_update'),
    url(r'^eureka/(?P<slug>[-\w]+)/instruction/step/(?P<step_slug>[-\w]+)/delete/', EurekaInstructionStepDeleteView.as_view(), name='eureka_instruction_step_delete'),

]
