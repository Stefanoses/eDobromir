from .models import ErrorReport
import django_filters

class ErrorReportFilter(django_filters.FilterSet):
    class Meta:
        model = ErrorReport
        fields = ['actual_state', 'error_login_state', 'error_code', 'error_type', 'error_link']