import django_tables2 as tables
from django.contrib.auth.models import User
from django.db.models import Count
from django.db.models.functions import Length
from django.db.models import Count
from django.db.models import F
from eureka.models import Eureka
from concept.models import Concept
from comments.models import Comment


class RankTable(tables.Table):
    position = tables.Column()

    class Meta:
        model = User

    def order_position(self, queryset, is_descending):
        queryset = queryset.annotate(
            position=F('rank__points')
        ).order_by(('-' if is_descending else '') + 'position')
        return (queryset, True)


class ActivityEurekaTable(tables.Table):
    class Meta:
        model = Eureka


class ActivityConceptTable(tables.Table):
    class Meta:
        model = Concept


class ActivityUserTable(tables.Table):
    class Meta:
        model = User