# -*- coding: utf-8 -*-
from django.shortcuts import render, redirect, render_to_response, HttpResponse, HttpResponseRedirect
from django.views.generic import ListView
from notification.models import NotificationModel, Notification
from guardian.mixins import PermissionRequiredMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.detail import DetailView
from django.views.generic.base import TemplateView, View
from django.views.generic import CreateView
from django.contrib.auth.models import User
from django.contrib import messages
from django.shortcuts import get_object_or_404
from django.conf import settings
from administration.models import BehaviorSettings
from notification.models import FollowersUserModel
from tags.models import DefaultTag, Sympathizer
from .tables import *
from .filters import *
from django_tables2 import RequestConfig
from .models import *
from .forms import *
from annoying.functions import get_object_or_None
from django.db.models import Q
from guardian.shortcuts import assign_perm
from guardian.mixins import PermissionRequiredMixin
from administration.views import RatelimitConversationCreateView


class NotificationListView(LoginRequiredMixin, ListView):
    model = NotificationModel
    template_name = 'notification_list.html'

    def dispatch(self, request, *args, **kwargs):
        self.get_queryset().filter(seeed_first=True).update(seeed_second=True)
        self.get_queryset().filter(seeed_first=False).update(seeed_first=True)
        return super(NotificationListView, self).dispatch(request, *args, **kwargs)

    def get_queryset(self):
        queryset = super(NotificationListView, self).get_queryset()
        queryset = queryset.get(user=self.request.user).container.all()
        return queryset

    def get_context_data(self, **kwargs):
        context = super(NotificationListView, self).get_context_data(**kwargs)
        filter = NotificationsFilter(self.request.GET, self.get_queryset())
        table = NotificationsTable(filter.qs, order_by='-published')
        RequestConfig(self.request, paginate={'per_page': 30}).configure(table)
        context['filter'] = filter
        context['table'] = table
        return context


class NotificationFollowers(LoginRequiredMixin, TemplateView):
    observe_object = None
    template_name = 'notification_followers.html'
    http_method_names = ['post']
    was_observer = None

    def handle_no_permission(self):
        messages.info(self.request, 'Musisz być zalogowany by móc obserwować.')
        super(NotificationFollowers, self).handle_no_permission()

    def post(self, request, *args, **kwargs):
        if self.observe_object:
            self.was_observer = self.observe_object.observers.container.filter(id=request.user.id).exists()
            if not self.was_observer and request.user:
                if self.observe_object != request.user:
                    self.observe_object.observers.container.add(request.user)
                    self.was_observer = True
                else:
                    messages.info(request, 'Nie możesz obserwować samego siebie.')
                    return HttpResponse(request, status=403)
            else:
                self.observe_object.observers.container.remove(request.user)
                self.was_observer = False


            return render_to_response(self.template_name, context=self.get_context_data(**kwargs))

    def get_context_data(self, **kwargs):
        context = super(NotificationFollowers, self).get_context_data(**kwargs)
        context['object'] = self.observe_object
        context['was_observer'] = self.was_observer
        return context

    def dispatch(self, request, *args, **kwargs):
        self.observe_object = User.objects.get(username=self.kwargs['username'])
        return super(NotificationFollowers, self).dispatch(request, *args, **kwargs)


class NotificationFollowTag(LoginRequiredMixin, TemplateView):
    observe_object = None
    template_name = 'notification_follow_tag.html'
    http_method_names = ['post']
    was_observer = None

    def handle_no_permission(self):
        messages.info(self.request, 'Musisz być zalogowany by móc obserwować.')
        super(NotificationFollowTag, self).handle_no_permission()

    def post(self, request, *args, **kwargs):
        if self.observe_object:
            self.was_observer = self.observe_object.observers.filter(id=request.user.id).exists()
            if not self.was_observer and request.user:
                self.observe_object.observers.add(request.user)
                self.was_observer = True
            else:
                self.observe_object.observers.remove(request.user)
                self.was_observer = False

            return render_to_response(self.template_name, context=self.get_context_data(**kwargs))

    def get_context_data(self, **kwargs):
        context = super(NotificationFollowTag, self).get_context_data(**kwargs)
        context['object'] = self.observe_object
        context['was_observer'] = self.was_observer
        context['observers_count'] = self.observe_object.observers.count()
        return context

    def dispatch(self, request, *args, **kwargs):
        self.observe_object = DefaultTag.objects.get(slug=self.kwargs['slug'])
        return super(NotificationFollowTag, self).dispatch(request, *args, **kwargs)


class NotificationFollowSympathizer(LoginRequiredMixin, TemplateView):
    observe_object = None
    template_name = 'notification_follow_sympathizer.html'
    http_method_names = ['post']
    was_observer = None

    def handle_no_permission(self):
        messages.info(self.request, 'Musisz być zalogowany by móc obserwować.')
        super(NotificationFollowSympathizer, self).handle_no_permission()

    def post(self, request, *args, **kwargs):
        if self.observe_object:
            self.was_observer = self.observe_object.observers.filter(id=request.user.id).exists()
            if not self.was_observer and request.user:
                self.observe_object.observers.add(request.user)
                self.was_observer = True
            else:
                self.observe_object.observers.remove(request.user)
                self.was_observer = False

            return render_to_response(self.template_name, context=self.get_context_data(**kwargs))

    def get_context_data(self, **kwargs):
        context = super(NotificationFollowSympathizer, self).get_context_data(**kwargs)
        context['object'] = self.observe_object
        context['was_observer'] = self.was_observer
        context['observers_count'] = self.observe_object.observers.count()
        return context

    def dispatch(self, request, *args, **kwargs):
        self.observe_object = Sympathizer.objects.get(slug=self.kwargs['slug'])
        return super(NotificationFollowSympathizer, self).dispatch(request, *args, **kwargs)


class NotificationAction(View):
    notification_target = None
    notification_actor = None

    def notification_action(self):
        pass


class NotificationPostAction(NotificationAction):
    def dispatch(self, request, *args, **kwargs):
        return super(NotificationPostAction, self).dispatch(request, *args, **kwargs)


class NotificationDispathAction(NotificationAction):
    def dispatch(self, request, *args, **kwargs):
        return super(NotificationDispathAction, self).dispatch(request, *args, **kwargs)


class NotificationBehaviorAction(NotificationAction):
    behavior_settings = None

    def notification_action(self):
        self.behavior_settings = get_object_or_404(BehaviorSettings, id=settings.ADMINISTRATION_BEHAVIOR_SETTINGS_ID)
        if self.notification_actor.num_vote_up >= self.behavior_settings.eureka_main_page_point and self.notification_actor.is_waiting == True:
            self.notification_actor.is_waiting = False
            self.notification_actor.save()
            self.notification_target.notifications.container.create(content = 'Twoja eureka dostała się na stronę główną',
                                                                    content_object = self.notification_actor)


class NotificationCommentAction(NotificationAction):
    comment_target = None
    comment_parent = None

    def notification_action(self):
        if self.notification_actor.created_by != self.notification_target:
            self.notification_target.notifications.container.create(content = 'Ktoś napisał do ciebie w komentarzu',
                                                                    content_object = self.notification_actor)


class NotificationNewContentAction(NotificationAction):
    def notification_action(self):
        created_by = User.objects.get(id=self.notification_actor.created_by.id)
        self.notification_target = created_by.observers.container.all()
        for follower in self.notification_target:
            follower.notifications.container.create(content='Użytkownik którego obserwujesz dodał nową treść',
                                                    content_object=self.notification_actor)

        tag_objs = self.notification_actor.tags.get_queryset()
        for tag in tag_objs:
            for follower in tag.observers.all():
                if follower != created_by:
                    follower.notifications.container.create(content='W tagu który obserwujesz dodano nową treść',
                                                            content_object=self.notification_actor)

        sympathizer_obj = self.notification_actor.sympathizers
        if sympathizer_obj:
            for follower in sympathizer_obj.observers.all():
                if follower != created_by:
                    follower.notifications.container.create(content='W tagu sympatyków który obserwujesz dodano nową treść',
                                                            content_object=self.notification_actor)



class ConversationCreateView(LoginRequiredMixin, RatelimitConversationCreateView, CreateView):
    model = Message
    fields = ['recipient', 'content']
    template_name = 'conversation_create.html'

    def form_valid(self, form):
        form.instance.sender = self.request.user
        if form.instance.recipient.username == 'AnonymousUser' or form.instance.sender == form.instance.recipient:
            return HttpResponseRedirect(self.get_failed_url())

        conversation = Conversation.objects.filter(owners__in=[form.instance.sender]).filter(owners__in=[form.instance.recipient]).first()
        if conversation:
            form.instance.conversation = conversation
        else:
            conversation = Conversation.objects.create()
            conversation.owners.add(form.instance.sender)
            conversation.owners.add(form.instance.recipient)
            form.instance.conversation = conversation
            assign_perm('notification.change_conversation', form.instance.sender, conversation)
            assign_perm('notification.change_conversation', form.instance.recipient, conversation)
        conversation.seeed.clear()
        return super(ConversationCreateView, self).form_valid(form)

    def get_failed_url(self):
        messages.info(self.request, 'Nie możesz wysłać wiadomości do tego użytkownika.')
        return reverse_lazy('notification:conversation_create')

    def get_success_url(self):
        self.object.conversation.messages.add(self.object)
        self.object.conversation.save()
        return reverse_lazy('notification:conversation_detail', kwargs={'pk': self.object.conversation.id})

    def get_context_data(self, **kwargs):
        context = super(ConversationCreateView, self).get_context_data(**kwargs)
        context['conversations'] = Conversation.objects.filter(owners__in=[self.request.user])
        return context


class ConversationDetailView(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    model = Conversation
    template_name = 'conversation_detail.html'
    context_object_name = 'conversation'
    permission_required = 'notification.change_conversation'
    raise_exception = True

    def get(self, request, *args, **kwargs):
        self.get_object().seeed.add(request.user)
        print 'asdasdasdasdasdasdasd'
        return super(ConversationDetailView, self).get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(ConversationDetailView, self).get_context_data(**kwargs)
        context['conversation_messages'] = Message.objects.filter(conversation=self.object).order_by('created')
        context['conversations'] = Conversation.objects.filter(owners__in=[self.request.user])
        return context