from django.contrib import admin
from .models import Linked


class LinkedAdmin(admin.ModelAdmin):
    list_display = ('title', 'link', 'created_by')
    search_fields = ('title', 'link', 'created_by', 'slug')
    ordering = ('-created',)
    date_hierarchy = 'created'
admin.site.register(Linked, LinkedAdmin)
