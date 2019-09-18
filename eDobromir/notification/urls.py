from django.conf.urls import url, include
from django.contrib import admin
from .views import *


urlpatterns = [
    url(r'^notification/list/$', NotificationListView.as_view(), name='notification_list'),
    url(r'^notification/follow/user/(?P<username>[-\w]+)/$', NotificationFollowers.as_view(), name='notification_observer'),
    url(r'^notification/follow/tag/(?P<slug>[-\w]+)/$', NotificationFollowTag.as_view(), name='notification_follow_tag'),
    url(r'^notification/follow/sympathizer/(?P<slug>[-\w]+)/$', NotificationFollowSympathizer.as_view(), name='notification_follow_sympathizer'),

    url(r'^conversation/create/$', ConversationCreateView.as_view(), name='conversation_create'),
    url(r'^conversation/(?P<pk>\d+)/detail/$', ConversationDetailView.as_view(), name='conversation_detail'),
]
