from django.shortcuts import render
from django.views.generic import ListView, TemplateView, DetailView, CreateView
from taggit.models import Tag
from search.tables import SearchTable
from django_tables2 import RequestConfig
from eureka.models import Eureka
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Sympathizer, DefaultTag
from django.template.defaultfilters import slugify
import itertools
from guardian.shortcuts import assign_perm
from django.shortcuts import get_object_or_404
from django.core.urlresolvers import reverse_lazy
from forms import SympathizerCreateForm


class TagListView(ListView):
    model = DefaultTag
    template_name = 'tags_list.html'
    context_object_name = 'tags'


class SympathizerListView(ListView):
    model = Sympathizer
    template_name = 'sympathizer_list.html'
    context_object_name = 'sympathizers'


class SympathizerCreateView(LoginRequiredMixin, CreateView):
    model = Sympathizer
    template_name = 'sympathizer_create.html'

    def get_form(self, form_class=None):
        return SympathizerCreateForm(self.request.user, self.request.POST)

    def form_valid(self, form):
        max_length_slug = Sympathizer._meta.get_field('slug').max_length
        slug = orig = slugify(form.instance.name)[0:max_length_slug]
        for x in itertools.count(1):
            if not Sympathizer.objects.filter(slug=slug).exists():
                break
            slug = "%s-%d" % (orig[:max_length_slug - len(str(x)) - 1], x)

        form.instance.name = slug
        form.instance.slug = slug
        form.instance.created_by = self.request.user
        if not form.instance.icon:
            form.instance.icon = 'exclamation'
        return super(SympathizerCreateView, self).form_valid(form)

    def get_success_url(self):
        assign_perm('tags.delete_sympathizer', self.object.created_by, self.object)
        assign_perm('tags.change_sympathizer', self.object.created_by, self.object)
        return reverse_lazy('account_profile_detail', kwargs={'username': self.object.created_by.username})