from django.contrib import admin
from .models import *


class CommentAdmin(admin.ModelAdmin):
    list_display = ('created_by', 'parent', 'created', 'slug')
    search_fields = ('created_by', 'parent', 'content', 'slug')
    ordering = ('-created',)
    date_hierarchy = 'created'
admin.site.register(Comment, CommentAdmin)
