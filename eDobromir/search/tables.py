import django_tables2 as tables
from eureka.models import Eureka
from django.db.models import F
from django.db.models import Count

class SearchTable(tables.Table):
    active = tables.Column()
    popular = tables.Column()

    class Meta:
        model = Eureka

    def order_active(self, queryset, is_descending):
        queryset = queryset.annotate(
            active=Count('comments')
        ).order_by(('-' if is_descending else '') + 'active')
        return (queryset, True)

    def order_popular(self, queryset, is_descending):
        queryset = queryset.annotate(
            popular=Count('votes')
        ).order_by(('-' if is_descending else '') + 'popular')
        return (queryset, True)

