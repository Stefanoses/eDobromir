from django.contrib import admin
from .models import *


class ConceptAdmin(admin.ModelAdmin):
    list_display = ('created_by', 'created', 'slug')
    search_fields = ('created_by', 'content', 'slug')
    ordering = ('-created',)
    date_hierarchy = 'created'
admin.site.register(Concept, ConceptAdmin)

