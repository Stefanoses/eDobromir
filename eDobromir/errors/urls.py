from django.conf.urls import url, include
from django.contrib import admin
from .views import *
from django.views.defaults import bad_request

urlpatterns = [
    url(r'^$', handler400),
    url(r'^$', handler403),
    url(r'^$', handler404),
    url(r'^$', handler500),
]