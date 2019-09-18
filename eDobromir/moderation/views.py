# -*- coding: utf-8 -*-

from django.shortcuts import HttpResponse
from django.views.generic import CreateView
from .models import Moderation
from .forms import ReportModerationForm
from eureka.models import Eureka
from django.core.urlresolvers import reverse_lazy
from django.contrib import messages
from concept.models import Concept
from django.contrib.auth.mixins import LoginRequiredMixin
from administration.views import RatelimitUserOrIpView
from django.forms.utils import ValidationError


class ModerationReportView(LoginRequiredMixin, RatelimitUserOrIpView, CreateView):
    model = Moderation
    form_class = ReportModerationForm
    moderation_object = None

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super(ModerationReportView, self).form_valid(form)

    def moderation_action(self):
        if not self.moderation_object.moderations.filter(created_by__in=[self.request.user.id]).exists():
            self.moderation_object.moderations.add(self.object)
            messages.info(self.request, 'Treść została zgłoszona prawidłowo')
        else:
            self.object.delete()
            messages.info(self.request, 'Już zgłosiłeś tą treść')


class ModerationReportEurekaView(ModerationReportView):
    def dispatch(self, request, *args, **kwargs):
        self.moderation_object = Eureka.objects.get(slug=self.kwargs['slug'])
        return super(ModerationReportEurekaView, self).dispatch(request, *args, **kwargs)

    def get_success_url(self):
        self.moderation_action()
        return reverse_lazy('eureka:eureka_detail', kwargs={'slug':self.kwargs['slug']})


class ModerationReportConceptView(ModerationReportView):
    def dispatch(self, request, *args, **kwargs):
        self.moderation_object = Concept.objects.get(slug=self.kwargs['slug'])
        return super(ModerationReportConceptView, self).dispatch(request, *args, **kwargs)

    def get_success_url(self):
        self.moderation_action()
        return reverse_lazy('concept:concept_detail', kwargs={'slug':self.kwargs['slug']})


class ModerationReportEurekaCommentView(ModerationReportView):
    def dispatch(self, request, *args, **kwargs):
        self.moderation_object = Eureka.objects.get(slug=self.kwargs['slug']).comments.get(slug=self.kwargs['comment_slug'])
        return super(ModerationReportEurekaCommentView, self).dispatch(request, *args, **kwargs)

    def get_success_url(self):
        self.moderation_action()
        return reverse_lazy('eureka:eureka_detail', kwargs={'slug':self.kwargs['slug']})


class ModerationReportConceptCommentView(ModerationReportView):
    def dispatch(self, request, *args, **kwargs):
        self.moderation_object = Concept.objects.get(slug=self.kwargs['slug']).comments.get(slug=self.kwargs['comment_slug'])
        return super(ModerationReportConceptCommentView, self).dispatch(request, *args, **kwargs)

    def get_success_url(self):
        self.moderation_action()
        return reverse_lazy('concept:concept_detail', kwargs={'slug':self.kwargs['slug']})