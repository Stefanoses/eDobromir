from django.contrib import admin
from .models import DefaultTag, Sympathizer


class DefaultTagAdmin(admin.ModelAdmin):
    list_display = ('name', 'icon', 'slug')
    search_fields = ('name', 'icon', 'slug')
admin.site.register(DefaultTag, DefaultTagAdmin)


class SympathizerAdmin(admin.ModelAdmin):
    list_display = ('created_by', 'name', 'icon', 'slug')
    search_fields = ('created_by', 'name', 'icon', 'slug')
    ordering = ('-created',)
    date_hierarchy = 'created'
admin.site.register(Sympathizer, SympathizerAdmin)