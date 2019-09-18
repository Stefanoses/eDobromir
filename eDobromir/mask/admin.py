from django.contrib import admin
from .models import DeleteMask


class DeleteMaskAdmin(admin.ModelAdmin):
    list_display = ('is_delete', 'delete_set_datetime', 'created')
    search_fields = ('is_delete', 'delete_set_datetime', 'created')
    ordering = ('-created',)
    date_hierarchy = 'created'
admin.site.register(DeleteMask, DeleteMaskAdmin)
