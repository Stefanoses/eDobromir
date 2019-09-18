from django.contrib import admin
from .models import ErrorReport


class ErrorReportAdmin(admin.ModelAdmin):
    list_display = ('actual_state', 'error_login_state', 'error_code', 'error_type')
    search_fields = ('actual_state', 'error_login_state', 'error_code', 'error_type')
    ordering = ('-created',)
    date_hierarchy = 'created'
admin.site.register(ErrorReport, ErrorReportAdmin)

