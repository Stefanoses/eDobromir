from django.shortcuts import render

from django.shortcuts import get_object_or_404
from django.views.generic.edit import CreateView, DeleteView
from .models import *
from django.core.urlresolvers import reverse_lazy
from django.template.defaultfilters import slugify
import itertools
from guardian.mixins import PermissionRequiredMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from guardian.shortcuts import assign_perm
from django.contrib.auth.models import Group
from diary.views import DiaryOpenView
from django.core.urlresolvers import reverse_lazy
from notification.views import NotificationNewContentAction
from administration.views import RatelimitConceptCreateView
from mask.models import DeleteMask
from forms import ConceptCreateForm
from tags.models import Sympathizer


class ConceptCreateView(LoginRequiredMixin, PermissionRequiredMixin, NotificationNewContentAction, CreateView):
    model = Concept
    form_class = ConceptCreateForm
    template_name = 'concept_create.html'

    permission_object = None
    permission_required = 'concept.add_concept'

    def form_valid(self, form):
        max_length_slug = Concept._meta.get_field('slug').max_length
        slug = orig = slugify(form.instance.content)[0:max_length_slug]
        for x in itertools.count(1):
            if not Concept.objects.filter(slug=slug).exists():
                break
            slug = "%s-%d" % (orig[:max_length_slug - len(str(x)) - 1], x)

        form.instance.slug = slug
        form.instance.created_by = self.request.user
        form.instance.mask = DeleteMask.objects.create()
        return super(ConceptCreateView, self).form_valid(form)

    def get_success_url(self):
        assign_perm('concept.is_owner', self.object.created_by, self.object)
        assign_perm('concept.delete_concept', self.object.created_by, self.object)
        assign_perm('concept.delete_concept', self.object.created_by, self.object)
        users_group = get_object_or_404(Group, name='users')
        assign_perm('concept.can_vote', users_group, self.object)
        self.notification_actor = self.object
        self.notification_action()
        return reverse_lazy('concept:concept_detail', kwargs={'slug':self.object.slug})


class ConceptDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Concept
    template_name = 'concept_delete.html'
    permission_object = None
    permission_required = 'concept.delete_concept'

    def get_permission_object(self):
        return self.get_object()

    def get_success_url(self):
        return reverse_lazy('search:search_concept')


class ConceptDetailView(DiaryOpenView):
    model = Concept
    template_name = 'concept_detail.html'