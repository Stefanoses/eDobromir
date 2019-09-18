# import django_filters
# from eureka.models import Eureka
# from django import forms
# from django_filters.widgets import BooleanWidget
#
#
# class EurekaFilter(django_filters.FilterSet):
#     class Meta:
#         model = Eureka
#         fields = ['published']
#
#
# class SearchFilter(django_filters.FilterSet):
#     search_eureka = django_filters.BooleanFilter(widget=BooleanWidget, method='search_eureka_filter')
#
#     def search_eureka_filter(self, queryset, name, value):
#         queryset = queryset | Eureka.objects.all()
#         return queryset