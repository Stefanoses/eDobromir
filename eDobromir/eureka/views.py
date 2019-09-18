# -*- coding: utf-8 -*-

from django.shortcuts import get_object_or_404
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.detail import DetailView
from .models import Eureka, EurekaInstruction, EurekaInstructionStep
from django.core.urlresolvers import reverse_lazy
from django.template.defaultfilters import slugify
import itertools
from guardian.mixins import PermissionRequiredMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from guardian.shortcuts import assign_perm, remove_perm
from django.utils import timezone
from django.contrib.auth.models import Group, User
from diary.views import DiaryOpenView
from django.forms.forms import ValidationError
from notification.views import *
from administration.views import RatelimitEurekaCreateView, RatelimitEurekaStepCreateView
from mask.models import DeleteMask
from .forms import EurekaCreateForm


class EurekaCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Eureka
    template_name = 'eureka_create.html'
    form_class = EurekaCreateForm

    permission_object = None
    permission_required = 'eureka.add_eureka'

    def form_valid(self, form):
        tags = form.cleaned_data['tags']
        if len(tags) > 5:
            raise ValidationError('Możesz wprowadzić maksymalnie 5 tagów.')

        max_length_slug = Eureka._meta.get_field('slug').max_length
        slug = orig = slugify(form.instance.title)[0:max_length_slug]
        for x in itertools.count(1):
            if not Eureka.objects.filter(slug=slug).exists():
                break
            slug = "%s-%d" % (orig[:max_length_slug - len(str(x)) - 1], x)

        form.instance.slug = slug
        form.instance.created_by = self.request.user
        form.instance.eurekaInstruction = EurekaInstruction.objects.create()
        form.instance.mask = DeleteMask.objects.create()
        return super(EurekaCreateView, self).form_valid(form)

    def get_success_url(self):
        assign_perm('eureka.is_owner', self.object.created_by, self.object)
        assign_perm('eureka.can_view', self.object.created_by, self.object)
        assign_perm('eureka.change_eureka', self.object.created_by, self.object)
        assign_perm('eureka.delete_eureka', self.object.created_by, self.object)
        return reverse_lazy('eureka:eureka_summary', kwargs={'slug':self.object.slug})


class EurekaUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Eureka
    fields = ['title', 'tags', 'sympathizers', 'description', 'link', 'preview_image', 'price', 'difficult', 'content_type']
    template_name = 'eureka_update.html'
    permission_required = 'eureka.change_eureka'
    raise_exception = True

    def get_success_url(self):
        return reverse_lazy('eureka:eureka_summary', kwargs={'slug':self.object.slug})


class EurekaDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Eureka
    template_name = 'eureka_delete.html'
    permission_required = 'eureka.delete_eureka'
    raise_exception = True

    def get_permission_object(self):
        return self.get_object()

    def get_success_url(self):
        return reverse_lazy('search:search_eureka')


class EurekaDetailView(PermissionRequiredMixin, DiaryOpenView):
    model = Eureka
    template_name = 'eureka_detail.html'
    permission_required = 'eureka.can_view'
    raise_exception = True

    def get_context_data(self, **kwargs):
        kwargs['active_page'] = 'eureka_detail'
        kwargs['eureka'] = self.object
        kwargs['order_by'] = self.request.GET.get('order_by')
        return kwargs


class EurekaInstructionDetailView(PermissionRequiredMixin, DetailView):
    model = Eureka
    template_name = 'eureka_instruction.html'
    permission_required = 'eureka.can_view'
    raise_exception = True

    def get_context_data(self, **kwargs):
        kwargs['eureka'] = self.object
        kwargs['active_page'] = 'eureka_instruction_detail'
        return kwargs


class EurekaInstructionStepCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = EurekaInstructionStep
    fields = ['title', 'content']
    template_name = 'eureka_instruction_step_create.html'
    eureka = None
    permission_required = 'eureka.change_eureka'
    raise_exception = True

    def get_permission_object(self):
        return self.eureka

    def dispatch(self, request, *args, **kwargs):
        self.eureka = Eureka.objects.get(slug=kwargs['slug'])
        return super(EurekaInstructionStepCreateView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(EurekaInstructionStepCreateView, self).get_context_data(**kwargs)
        context['eureka'] = self.eureka
        return context

    def form_valid(self, form):
        all_steps = self.eureka.eurekaInstruction.steps.all()
        max_length_slug = EurekaInstructionStep._meta.get_field('step_slug').max_length
        step_slug = orig = slugify(form.instance.title)[0:max_length_slug]
        for x in itertools.count(1):
            if not all_steps.filter(step_slug=step_slug).exists():
                break
            step_slug = "%s-%d" % (orig[:max_length_slug - len(str(x)) - 1], x)

        form.instance.step_slug = step_slug
        return super(EurekaInstructionStepCreateView, self).form_valid(form)

    def get_success_url(self):
        self.eureka.eurekaInstruction.steps.add(self.object)
        return reverse_lazy('eureka:eureka_instruction_step_update', kwargs={'slug':self.eureka.slug, 'step_slug': self.object.step_slug})


class EurekaInstructionStepUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = EurekaInstructionStep
    fields = ['title', 'content']
    template_name = 'eureka_instruction_step_update.html'
    eureka = None
    permission_required = 'eureka.change_eureka'
    raise_exception = True

    def get_permission_object(self):
        return self.eureka

    def dispatch(self, request, *args, **kwargs):
        self.eureka = Eureka.objects.get(slug=kwargs['slug'])
        return super(EurekaInstructionStepUpdateView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(EurekaInstructionStepUpdateView, self).get_context_data(**kwargs)
        context['eureka'] = self.eureka
        return context

    def get_object(self, queryset=None):
        step_slug = self.kwargs['step_slug']
        return EurekaInstructionStep.objects.get(step_slug=step_slug, eurekainstruction=self.eureka.eurekaInstruction)

    def get_success_url(self):
        return reverse_lazy('eureka:eureka_instruction_step_update', kwargs={'slug':self.eureka.slug, 'step_slug': self.object.step_slug})

    def form_valid(self, form):
        all_steps = self.eureka.eurekaInstruction.steps.all()
        max_length_slug = EurekaInstructionStep._meta.get_field('step_slug').max_length
        step_slug = orig = slugify(form.instance.title)[0:max_length_slug]
        for x in itertools.count(1):
            if not all_steps.filter(step_slug=step_slug).exists():
                break
            step_slug = "%s-%d" % (orig[:max_length_slug - len(str(x)) - 1], x)

        form.instance.step_slug = step_slug
        return super(EurekaInstructionStepUpdateView, self).form_valid(form)


class EurekaInstructionStepDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = EurekaInstructionStep
    fields = ['title']
    template_name = 'eureka_instruction_step_delete.html'
    eureka = None
    permission_required = 'eureka.change_eureka'
    raise_exception = True

    def get_permission_object(self):
        return self.eureka

    def dispatch(self, request, *args, **kwargs):
        self.eureka = Eureka.objects.get(slug=kwargs['slug'])
        return super(EurekaInstructionStepDeleteView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(EurekaInstructionStepDeleteView, self).get_context_data(**kwargs)
        context['eureka'] = self.eureka
        return context

    def get_object(self, queryset=None):
        step_slug = self.kwargs['step_slug']
        return EurekaInstructionStep.objects.get(step_slug=step_slug, eurekainstruction=self.eureka.eurekaInstruction)

    def get_success_url(self):
        return reverse_lazy('eureka:eureka_instruction_step_create', kwargs={'slug':self.eureka.slug})


class EurekaSummaryView(LoginRequiredMixin, PermissionRequiredMixin, NotificationNewContentAction, UpdateView):
    model = Eureka
    fields = ['is_published']
    template_name = 'eureka_summary.html'
    permission_required = 'eureka.is_owner'
    raise_exception = True

    def form_valid(self, form):
        form.instance.is_published = True
        form.instance.published = timezone.now()
        users_group = get_object_or_404(Group, name='users')
        anonymous_users = get_object_or_404(User, username='AnonymousUser')
        assign_perm('eureka.can_vote', users_group, self.object)
        assign_perm('eureka.can_view', users_group, self.object)
        assign_perm('eureka.can_view', anonymous_users, self.object)
        return super(EurekaSummaryView, self).form_valid(form)

    def get_success_url(self):
        self.notification_actor = self.object
        self.notification_action()
        return reverse_lazy('eureka:eureka_summary', kwargs={'slug': self.object.slug})
