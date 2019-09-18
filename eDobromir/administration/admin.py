from django.contrib import admin
from .models import BehaviorSettings


class BehaviorSettingsAdmin(admin.ModelAdmin):
    pass
admin.site.register(BehaviorSettings, BehaviorSettingsAdmin)