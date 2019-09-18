from django.conf.urls import url, include
from django.contrib import admin
from .views import ContentAddView
from django.views.generic.base import TemplateView
from .views import *


urlpatterns = [
    url(r'^content/$', ContentAddView.as_view(), name='content_add'),
    url(r'^idea/$', TemplateView.as_view(template_name='content_idea_site.html'), name='content_idea'),
    url(r'^cookies/$', TemplateView.as_view(template_name='content_cookies.html'), name='content_cookies'),
    url(r'^policy/$', TemplateView.as_view(template_name='content_policy.html'), name='content_policy'),
    url(r'^help/$', TemplateView.as_view(template_name='content_help.html'), name='content_help'),
    url(r'^contact/$', ContentContactView.as_view(), name='content_contact'),
    url(r'^cooperation/$', TemplateView.as_view(template_name='content_cooperation.html'), name='content_cooperation'),
    url(r'^regulations/$', TemplateView.as_view(template_name='content_regulations.html'), name='content_regulations'),

    url(r'^error/create/$', ContentErrorReportCreate.as_view(), name='content_error_create'),
    url(r'^error/list/$', ContentErrorReportList.as_view(), name='content_error_list'),
    url(r'^error/(?P<pk>\d+)/$', ContentErrorReportDetail.as_view(), name='content_error_detail'),
    url(r'^error/(?P<pk>\d+)/update/$', ContentErrorReportUpdate.as_view(), name='content_error_update'),
    url(r'^error/(?P<pk>\d+)/delete/$', ContentErrorReportDelete.as_view(), name='content_error_delete'),
]
