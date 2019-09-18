from django.contrib import admin
from .models import Notification, FollowersModel, FollowersUserModel, NotificationModel


class NotificationAdmin(admin.ModelAdmin):
    list_display = ('content', 'content_type', 'content_object')
    search_fields = ('content', 'content_type', 'content_object', 'object_id', 'seeed_first', 'seeed_second')
    ordering = ('-created',)
    date_hierarchy = 'created'
admin.site.register(Notification, NotificationAdmin)


class FollowersModelAdmin(admin.ModelAdmin):
    pass
admin.site.register(FollowersModel, FollowersModelAdmin)


class FollowersUserModelAdmin(admin.ModelAdmin):
    list_display = ('id', 'user')
    search_fields = ('id', 'container', 'user')
    ordering = ('-id',)
admin.site.register(FollowersUserModel, FollowersUserModelAdmin)


class NotificationModelAdmin(admin.ModelAdmin):
    list_display = ('id', 'user')
    search_fields = ('id', 'container', 'user')
    ordering = ('-id',)
admin.site.register(NotificationModel, NotificationModelAdmin)