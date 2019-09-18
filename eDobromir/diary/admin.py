from django.contrib import admin
from .models import *


class DiaryAdmin(admin.ModelAdmin):
    list_display = ('ip', 'session')
    search_fields = ('ip', 'session')
    ordering = ('-created',)
    date_hierarchy = 'created'
admin.site.register(Diary, DiaryAdmin)