from django.conf.urls import url, include
from django.contrib import admin
from .views import *


urlpatterns = [
    url(r'^eureka/(?P<slug>[-\w]+)/favorites/$', FavoritesManageEurekaView.as_view(), name='favorites_eureka'),
    url(r'^concept/(?P<slug>[-\w]+)/favorites/$', FavoritesManageConceptView.as_view(), name='favorites_concept'),
]
