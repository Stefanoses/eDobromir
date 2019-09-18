from django.contrib import admin
from .models import Moderation


class ModerationAdmin(admin.ModelAdmin):
    list_display = ('created_by', 'choiceReason')
    search_fields = ('created_by', 'choiceReason', 'reason', 'created')
    ordering = ('-created',)
    date_hierarchy = 'created'
admin.site.register(Moderation, ModerationAdmin)

