from .models import Notification
import django_filters


class NotificationsFilter(django_filters.FilterSet):
    class Meta:
        model = Notification
        fields = ['content']