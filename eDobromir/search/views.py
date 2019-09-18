from .tables import SearchTable
from django_tables2 import RequestConfig
from django.views.generic import TemplateView
from eureka.models import Eureka
from concept.models import Concept
from django.utils.timezone import timedelta, now
from django.views.generic.list import ListView


class SearchEurekaView(ListView):
    model = Eureka
    template_name = 'search_eureka.html'

    def get_queryset(self):
        queryset = super(SearchEurekaView, self).get_queryset()
        queryset = queryset.filter(is_waiting=False, is_published=True)
        return queryset

    def get_context_data(self, **kwargs):
        table = SearchTable(self.get_queryset(), order_by='-published')
        RequestConfig(self.request, paginate={'per_page': 30}).configure(table)
        contex = super(SearchEurekaView, self).get_context_data(**kwargs)
        contex['active_page'] = 'search_eureka'
        contex['table'] = table
        return contex


class SearchEurekaWaitingView(ListView):
    model = Eureka
    template_name = 'search_eureka_waiting.html'

    def get_queryset(self):
        queryset = super(SearchEurekaWaitingView, self).get_queryset()
        queryset = queryset.filter(is_waiting=True, is_published=True)
        return queryset

    def get_context_data(self, **kwargs):
        table = SearchTable(self.get_queryset(), order_by='-popular')
        RequestConfig(self.request, paginate={'per_page': 30}).configure(table)
        contex = super(SearchEurekaWaitingView, self).get_context_data(**kwargs)
        contex['active_page'] = 'search_eureka_waiting'
        contex['table'] = table
        return contex


class SearchConceptView(ListView):
    model = Concept
    template_name = 'search_concept.html'

    def get_queryset(self):
        queryset = super(SearchConceptView, self).get_queryset()
        return queryset

    def get_context_data(self, **kwargs):
        table = SearchTable(self.get_queryset(), order_by='-active')
        RequestConfig(self.request, paginate={'per_page': 30}).configure(table)
        contex = super(SearchConceptView, self).get_context_data(**kwargs)
        contex['active_page'] = 'search_concept'
        contex['table'] = table
        return contex


class SearchMixedView(TemplateView):
    search_input = None
    split = None
    tags = None
    users = None
    text = None
    sympathizers = None

    when_convert = None

    def dispatch(self, request, *args, **kwargs):
        self.split = []
        self.tags = []
        self.users = []
        self.text = []
        self.sympathizers = []

        self.when = request.GET.get('when') or ''
        self.how = request.GET.get('sort') or ''
        if self.when:
            if self.when == 'day':
                self.when_convert = now() - timedelta(days=1)
            if self.when == 'week':
                self.when_convert = now() - timedelta(days=7)
            if self.when == 'month':
                self.when_convert = now() - timedelta(days=30)
            if self.when == 'year':
                self.when_convert = now() - timedelta(days=360)
            if self.when == 'eternity':
                self.when_convert = now() - timedelta(days=360 * 20)

        self.search_input = request.GET.get('search_input') or ''
        if self.search_input:
            self.split = self.search_input.split(' ')
            for split_item in self.split:
                if '#' in split_item:
                    tag = split_item.replace('#', '')
                    self.tags.append(tag)
                elif '@' in split_item:
                    user = split_item.replace('@', '')
                    self.users.append(user)
                elif '!' in split_item:
                    sympathizer = split_item.replace('!', '')
                    self.sympathizers.append(sympathizer)
                else:
                    self.text.append(split_item)
        return super(SearchMixedView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = kwargs
        context['active_page'] = 'search_mixed'
        context['search_input'] = self.search_input
        context['tags'] = self.tags
        context['sympathizers'] = self.sympathizers
        context['when'] = self.when
        context['how'] = self.how
        return context


class SearchMixedEurekaView(SearchMixedView):
    template_name = 'search_mixed_eureka.html'

    def get_queryset(self):
        queryset = Eureka.objects.filter(is_waiting=False, is_published=True)
        if self.when_convert:
            queryset = queryset.filter(published__gte=self.when_convert)
        if self.search_input:
            for user in self.users:
                queryset = queryset.filter(created_by__username=user)
            for tag in self.tags:
                queryset = queryset.filter(tags__name__in=[tag])
            for sympathizer in self.sympathizers:
                queryset = queryset.filter(sympathizers__name__in=[sympathizer])
            for word in self.text:
                queryset = queryset.filter(title__icontains=word)
        return queryset

    def get_context_data(self, **kwargs):
        context = super(SearchMixedEurekaView, self).get_context_data(**kwargs)
        table = SearchTable(self.get_queryset(), order_by=self.how)
        RequestConfig(self.request, paginate={'per_page': 30}).configure(table)
        context['table'] = table
        context['where'] = 'eureka'
        return context


class SearchMixedEurekaWaitingView(SearchMixedView):
    template_name = 'search_mixed_eureka_waiting.html'

    def get_queryset(self):
        queryset = Eureka.objects.filter(is_waiting=True, is_published=True)
        if self.when_convert:
            queryset = queryset.filter(published__gte=self.when_convert)
        if self.search_input:
            for user in self.users:
                queryset = queryset.filter(created_by__username=user)
            for tag in self.tags:
                queryset = queryset.filter(tags__name__in=[tag])
            for sympathizer in self.sympathizers:
                queryset = queryset.filter(sympathizers__name__in=[sympathizer])
            for word in self.text:
                queryset = queryset.filter(title__icontains=word)
        return queryset

    def get_context_data(self, **kwargs):
        context = super(SearchMixedEurekaWaitingView, self).get_context_data(**kwargs)
        table = SearchTable(self.get_queryset(), order_by=self.how)
        RequestConfig(self.request, paginate={'per_page': 30}).configure(table)
        context['table'] = table
        context['where'] = 'eureka_waiting'
        return context


class SearchMixedConceptView(SearchMixedView):
    template_name = 'search_mixed_concept.html'

    def get_queryset(self):
        queryset = Concept.objects.all()
        if self.when_convert:
            queryset = queryset.filter(published__gte=self.when_convert)
        if self.search_input:
            for user in self.users:
                queryset = queryset.filter(created_by__username=user)
            for tag in self.tags:
                queryset = queryset.filter(tags__name__in=[tag])
            for sympathizer in self.sympathizers:
                queryset = queryset.filter(sympathizers__name__in=[sympathizer])
            for word in self.text:
                queryset = queryset.filter(content__icontains=word)
        return queryset

    def get_context_data(self, **kwargs):
        context = super(SearchMixedConceptView, self).get_context_data(**kwargs)
        table = SearchTable(self.get_queryset(), order_by=self.how)
        RequestConfig(self.request, paginate={'per_page': 30}).configure(table)
        context['table'] = table
        context['where'] = 'concept'
        return context


class SearchMixedEverywhereView(SearchMixedEurekaView, SearchMixedEurekaWaitingView, SearchMixedConceptView):
    template_name = 'search_mixed_everywhere.html'

    def get_context_data(self, **kwargs):
        context = super(SearchMixedEverywhereView, self).get_context_data(**kwargs)

        table_eureka = SearchTable(SearchMixedEurekaView.get_queryset(self), order_by=self.how)
        RequestConfig(self.request, paginate={'per_page': 10}).configure(table_eureka)

        table_eureka_waiting = SearchTable(SearchMixedEurekaWaitingView.get_queryset(self), order_by=self.how)
        RequestConfig(self.request, paginate={'per_page': 10}).configure(table_eureka_waiting)

        table_concept = SearchTable(SearchMixedConceptView.get_queryset(self), order_by=self.how)
        RequestConfig(self.request, paginate={'per_page': 10}).configure(table_concept)

        context['table_eureka'] = table_eureka
        context['table_eureka_waiting'] = table_eureka_waiting
        context['table_concept'] = table_concept
        context['where'] = 'everywhere'
        return context
