from django.core.urlresolvers import reverse_lazy
from django.shortcuts import get_object_or_404, HttpResponseRedirect
from django.views.generic.edit import CreateView, DeleteView
from django.views.generic.detail import DetailView
from django.views.generic.base import TemplateView
from .models import Comment
from eureka.models import Eureka
from .forms import CommentCreateForm, CommentReplyForm
from concept.models import Concept
from django.contrib.auth.mixins import LoginRequiredMixin
from ratelimit.mixins import RatelimitMixin
from administration.views import RatelimitCommentsCreateView, RatelimitCommentsReplyView
from notification.views import NotificationCommentAction
from mask.models import DeleteMask
from guardian.shortcuts import assign_perm
from guardian.mixins import PermissionRequiredMixin


class CommentCreateView(LoginRequiredMixin, RatelimitCommentsCreateView, NotificationCommentAction, CreateView):
    model = Comment
    form_class = CommentCreateForm
    comment_target = None

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        form.instance.mask = DeleteMask.objects.create()
        return super(CommentCreateView, self).form_valid(form)

    def get_success_url(self):
        assign_perm('comment.delete_comment', self.object.created_by, self.object)
        self.comment_target.comments.add(self.object)
        self.notification_target = self.comment_target.created_by
        self.notification_actor = self.object
        self.notification_action()
        return super(CommentCreateView, self).get_success_url()


class CommentReplyView(LoginRequiredMixin, RatelimitCommentsReplyView, NotificationCommentAction, CreateView):
    model = Comment
    form_class = CommentReplyForm

    def dispatch(self, request, *args, **kwargs):
        self.comment_parent = get_object_or_404(Comment, slug=self.kwargs['comment_slug'])
        return super(CommentReplyView, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        form.instance.parent = self.comment_parent
        form.instance.mask = DeleteMask.objects.create()
        return super(CommentReplyView, self).form_valid(form)

    def get_success_url(self):
        assign_perm('comment.delete_comment', self.object.created_by, self.object)
        self.comment_target.comments.add(self.object)
        self.notification_target = self.comment_parent.created_by
        self.notification_actor = self.object
        self.notification_action()
        return super(CommentReplyView, self).get_success_url()


class CommentDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Comment
    permission_required = 'comments.delete_comment'
    raise_exception = True
    parent_container = None

    def delete(self, request, *args, **kwargs):
        self.get_object().mask.set_delete(True)
        return HttpResponseRedirect(self.get_success_url())

    def get_object(self, queryset=None):
        return get_object_or_404(Comment, slug=self.kwargs['comment_slug'])

    def get_context_data(self, **kwargs):
        context = super(CommentDeleteView, self).get_context_data(**kwargs)
        context['comment_object'] = self.parent_container
        context['node'] = self.get_object()
        return context


class CommentEurekaDeleteView(CommentDeleteView):
    template_name = 'comments_eureka_delete.html'

    def get_object(self, queryset=None):
        return get_object_or_404(Comment, slug=self.kwargs['comment_slug'])

    def dispatch(self, request, *args, **kwargs):
        self.parent_container = get_object_or_404(Eureka, slug=self.kwargs['slug'])
        return super(CommentEurekaDeleteView, self).dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return reverse_lazy('eureka:eureka_detail', kwargs={'slug': self.parent_container.slug})


class CommentConceptDeleteView(CommentDeleteView):
    template_name = 'comments_concept_delete.html'

    def dispatch(self, request, *args, **kwargs):
        self.parent_container = get_object_or_404(Concept, slug=self.kwargs['slug'])
        return super(CommentConceptDeleteView, self).dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return reverse_lazy('concept:concept_detail', kwargs={'slug': self.parent_container.slug})


class CommentEurekaCreateView(CommentCreateView):
    def dispatch(self, request, *args, **kwargs):
        self.comment_target = get_object_or_404(Eureka, slug=self.kwargs['slug'])
        self.success_url = reverse_lazy('eureka:eureka_detail', args={self.kwargs['slug']})
        return super(CommentEurekaCreateView, self).dispatch(request, *args, **kwargs)


class CommentEurekaReplyView(CommentReplyView):
    def dispatch(self, request, *args, **kwargs):
        self.comment_target = get_object_or_404(Eureka, slug=self.kwargs['slug'])
        self.success_url = reverse_lazy('eureka:eureka_detail', args={self.kwargs['slug']})
        return super(CommentEurekaReplyView, self).dispatch(request, *args, **kwargs)


class CommentConceptCreateView(CommentCreateView):
    def dispatch(self, request, *args, **kwargs):
        self.comment_target = get_object_or_404(Concept, slug=self.kwargs['slug'])
        self.success_url = reverse_lazy('concept:concept_detail', args={self.kwargs['slug']})
        return super(CommentConceptCreateView, self).dispatch(request, *args, **kwargs)


class CommentConceptReplyView(CommentReplyView):
    def dispatch(self, request, *args, **kwargs):
        self.comment_target = get_object_or_404(Concept, slug=self.kwargs['slug'])
        self.success_url = reverse_lazy('concept:concept_detail', args={self.kwargs['slug']})
        return super(CommentConceptReplyView, self).dispatch(request, *args, **kwargs)