# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.views.generic import TemplateView, CreateView, DetailView, ListView, UpdateView, DeleteView, FormView
from .models import ErrorReport
from .forms import ErrorReportForm, ContactForm
from django.core.urlresolvers import reverse_lazy
from django_tables2.tables import Table
from .filters import ErrorReportFilter
from .tables import ErrorReportTable
from django_tables2 import RequestConfig
from django.contrib import messages
from guardian.mixins import PermissionRequiredMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.mail import send_mail
from django.core.mail import EmailMessage
from administration.views import RatelimitContentErrorReportCreateView, RatelimitContentContactView


class ContentAddView(TemplateView):
    template_name = 'content_add.html'

    def get_context_data(self, **kwargs):
        context = super(ContentAddView, self).get_context_data(**kwargs)
        context['active_page'] = 'content_add'
        return context


class ContentErrorReportCreate(RatelimitContentErrorReportCreateView, CreateView):
    model = ErrorReport
    form_class = ErrorReportForm

    def get_success_url(self):
        messages.success(self.request, 'Pomyślnie zgłoszono błąd')
        return reverse_lazy('content:content_error_detail', kwargs={'pk': self.object.id})


class ContentErrorReportDetail(DetailView):
    template_name = 'content_error_report_detail.html'
    model = ErrorReport


class ContentErrorReportList(ListView):
    template_name = 'content_error_report_list.html'
    model = ErrorReport

    def get_context_data(self, **kwargs):
        context = super(ContentErrorReportList, self).get_context_data(**kwargs)
        filter = ErrorReportFilter(self.request.GET, self.get_queryset())
        table = ErrorReportTable(filter.qs)
        RequestConfig(self.request, paginate={'per_page': 30}).configure(table)
        context['filter'] = filter
        context['table'] = table
        return context


class ContentErrorReportUpdate(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    template_name = 'content_error_report_update.html'
    model = ErrorReport
    fields = ['actual_state', 'comment_admin']
    permission_required = 'content.change_errorreport'
    raise_exception = True

    def get_success_url(self):
        messages.success(self.request, 'Pomyślnie zaktualizowano błąd')
        return reverse_lazy('content:content_error_detail', kwargs={'pk': self.object.id})


class ContentErrorReportDelete(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    template_name = 'content_error_report_delete.html'
    model = ErrorReport
    permission_required = 'content.delete_errorreport'
    raise_exception = True

    def get_success_url(self):
        messages.success(self.request, 'Pomyślnie usunięto błąd')
        return reverse_lazy('content:content_error_list')


class ContentContactView(FormView):
    template_name = 'content_contact.html'
    form_class = ContactForm

    def form_valid(self, form):
        name = form.cleaned_data['name']
        email = form.cleaned_data['email']
        message = form.cleaned_data['message']
        send_mail('Zapytanie kontaktowe od ' + name + ' z eDobromir',
                  message,
                  '(eDobromir) hello@edobromir.pl',
                  ['hello@edobromir.pl', email],
                  fail_silently=False)
        return super(ContentContactView, self).form_valid(form)

    def get_success_url(self):
        messages.success(self.request, 'Pomyślnie wysłano wiadomość')
        return reverse_lazy('content:content_contact')

