from django.views.generic import CreateView
from .models import Linked
from .forms import LinkedCreateForm
from django.shortcuts import get_object_or_404
from eureka.models import Eureka
from django.template.defaultfilters import slugify
import itertools
from concept.models import Concept
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.urlresolvers import reverse_lazy
from administration.views import RatelimitLinkedCreateView
from mask.models import DeleteMask


class LinkedCreateView(LoginRequiredMixin, RatelimitLinkedCreateView, CreateView):
    model = Linked
    form_class = LinkedCreateForm
    parent = None

    def form_valid(self, form):
        max_length_slug = Linked._meta.get_field('slug').max_length
        slug = orig = slugify(form.instance.title + self.parent.slug)[0:max_length_slug]
        for x in itertools.count(1):
            if not Linked.objects.filter(slug=slug).exists():
                break
            slug = "%s-%d" % (orig[:max_length_slug - len(str(x)) - 1], x)

        form.instance.slug = slug
        form.instance.created_by = self.request.user
        form.instance.mask = DeleteMask.objects.create()
        return super(LinkedCreateView, self).form_valid(form)


class LinkedEurekaCreateView(LinkedCreateView):
    def dispatch(self, request, *args, **kwargs):
        self.parent = get_object_or_404(Eureka, slug=self.kwargs['slug'])
        return super(LinkedEurekaCreateView, self).dispatch(request, *args, **kwargs)

    def get_success_url(self):
        self.parent.links.add(self.object)
        return reverse_lazy('eureka:eureka_detail', args={self.kwargs['slug']})


class LinkedConceptCreateView(LinkedCreateView):
    def dispatch(self, request, *args, **kwargs):
        self.parent = get_object_or_404(Concept, slug=self.kwargs['slug'])
        return super(LinkedConceptCreateView, self).dispatch(request, *args, **kwargs)

    def get_success_url(self):
        self.parent.links.add(self.object)
        return reverse_lazy('concept:concept_detail', args={self.kwargs['slug']})