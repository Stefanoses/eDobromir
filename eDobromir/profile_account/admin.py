from django.contrib import admin
from .models import Settings, SettingsAvatar, SettingsProfile, Rank


class SettingsProfileAdmin(admin.ModelAdmin):
    list_display = ('name', 'last_name', 'public_email', 'website', 'town')
    search_fields = ('name', 'last_name', 'public_email', 'website', 'town', 'description')
admin.site.register(SettingsProfile, SettingsProfileAdmin)


class SettingsAvatarAdmin(admin.ModelAdmin):
    pass
admin.site.register(SettingsAvatar, SettingsAvatarAdmin)


class SettingsAdmin(admin.ModelAdmin):
    list_display = ('user', 'profile', 'avatar')
    search_fields = ('user', 'profile', 'avatar')
admin.site.register(Settings, SettingsAdmin)


class RankAdmin(admin.ModelAdmin):
    list_display = ('user', 'points')
    search_fields = ('user', 'points')
admin.site.register(Rank, RankAdmin)