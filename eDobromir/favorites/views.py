# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, render_to_response
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.base import TemplateView, View
from django.contrib import messages
from django.shortcuts import get_object_or_404
from eureka.models import Eureka
from concept.models import Concept
from django.contrib.contenttypes.models import ContentType


class FavoritesManageView(LoginRequiredMixin, TemplateView):
    favorite_content = None
    was_favorite = None
    http_method_names = ['post']

    def handle_no_permission(self):
        messages.info(self.request, 'Musisz być zalogowany by móc dodawać ulubione.')
        super(FavoritesManageView, self).handle_no_permission()

    def post(self, request, *args, **kwargs):
        if self.favorite_content:
            self.was_favorite = self.favorite_content.favorites.filter(id=request.user.id).exists()
            if not self.was_favorite and request.user:
                self.favorite_content.favorites.add(request.user)
                self.was_favorite = True
            else:
                self.favorite_content.favorites.remove(request.user)
                self.was_favorite = False

            return render_to_response(self.template_name, context=self.get_context_data(**kwargs))

    def get_context_data(self, **kwargs):
        context = super(FavoritesManageView, self).get_context_data(**kwargs)
        context['favorite_content'] = self.favorite_content
        context['was_favorite'] = self.was_favorite
        return context


class FavoritesManageEurekaView(FavoritesManageView):
    template_name = 'favorites_manage_eureka.html'

    def dispatch(self, request, *args, **kwargs):
        self.favorite_content = get_object_or_404(Eureka, slug=kwargs['slug'])
        return super(FavoritesManageEurekaView, self).dispatch(request, *args, **kwargs)


class FavoritesManageConceptView(FavoritesManageView):
    template_name = 'favorites_manage_concept.html'

    def dispatch(self, request, *args, **kwargs):
        self.favorite_content = get_object_or_404(Concept, slug=kwargs['slug'])
        return super(FavoritesManageConceptView, self).dispatch(request, *args, **kwargs)