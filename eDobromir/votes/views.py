# -*- coding: utf-8 -*-

from administration.views import RatelimitVoteActionView
from notification.views import *


class VoteDetailView(DetailView):
    def get_context_data(self, **kwargs):
        contex = super(VoteDetailView, self).get_context_data(**kwargs)
        contex['was_voting'] = self.object.votes.exists(self.request.user.id)
        return contex

    def get_object(self, queryset=None):
        return self.model.objects.get(slug=self.kwargs['slug'])


class VoteDetailEurekaView(VoteDetailView):
    model = Eureka
    template_name = 'vote_eureka.html'


class VoteDetailConceptView(VoteDetailView):
    model = Concept
    template_name = 'vote_concept.html'


class VoteActionView(LoginRequiredMixin, RatelimitVoteActionView, TemplateView):
    vote_object = None
    template_name = ''
    http_method_names = ['post']
    was_voting = None
    raise_exception = True

    def handle_no_permission(self):
        messages.info(self.request, 'Musisz być zalogowany by móc głosować')
        super(VoteActionView, self).handle_no_permission()

    def post(self, request, *args, **kwargs):
        if self.vote_object:
            if not self.vote_object.mask.is_delete:
                self.vote_action()
            else:
                messages.info(self.request, 'Nie możesz głosowac na usunięte treści')
            return render_to_response(self.template_name, context=self.get_context_data(**kwargs))

    def get_context_data(self, **kwargs):
        context = super(VoteActionView, self).get_context_data(**kwargs)
        context['object'] = self.vote_object
        context['was_voting'] = self.was_voting
        context['request'] = self.request
        return context

    def vote_action(self):
        pass

    def get_vote_object(self):
        return self.vote_object

    def success_vote(self):
        pass


class VoteUpView(VoteActionView):
    can_vote = True

    def vote_action(self):
        if self.vote_object.created_by == self.request.user:
            self.can_vote = False

        self.was_voting = self.vote_object.votes.exists(self.request.user.id)
        if self.was_voting:
            self.can_vote = False

        if self.can_vote:
            self.was_voting = True
            self.vote_object.votes.up(self.request.user.id)
            self.vote_object.created_by.rank.up()
            self.success_vote()



class VoteUpEurekaView(VoteUpView, NotificationBehaviorAction):
    template_name = 'vote_eureka.html'

    def dispatch(self, request, *args, **kwargs):
        self.vote_object = get_object_or_404(Eureka, slug=kwargs['slug'])
        self.notification_target = self.vote_object.created_by
        self.notification_actor = self.vote_object
        return super(VoteUpEurekaView, self).dispatch(request, *args, **kwargs)

    def success_vote(self):
        self.notification_action()


class VoteUpConceptView(VoteUpView):
    template_name = 'vote_concept.html'

    def dispatch(self, request, *args, **kwargs):
        self.vote_object = get_object_or_404(Concept, slug=kwargs['slug'])
        return super(VoteUpConceptView, self).dispatch(request, *args, **kwargs)


class VoteUpEurekaLinkedView(VoteUpView):
    template_name = 'vote_eureka_linked.html'

    def dispatch(self, request, *args, **kwargs):
        eureka = get_object_or_404(Eureka, slug=kwargs['slug'])
        kwargs['eureka'] = eureka
        self.vote_object = eureka.links.get(slug=self.kwargs['linked_slug'])
        return super(VoteUpEurekaLinkedView, self).dispatch(request, *args, **kwargs)


class VoteUpConceptLinkedView(VoteUpView):
    template_name = 'vote_concept_linked.html'

    def dispatch(self, request, *args, **kwargs):
        concept = get_object_or_404(Concept, slug=kwargs['slug'])
        kwargs['concept'] = concept
        self.vote_object = concept.links.get(slug=self.kwargs['linked_slug'])
        return super(VoteUpConceptLinkedView, self).dispatch(request, *args, **kwargs)


class VoteUpEurekaCommentView(VoteUpView):
    template_name = 'vote_eureka_comment.html'

    def dispatch(self, request, *args, **kwargs):
        eureka = get_object_or_404(Eureka, slug=kwargs['slug'])
        kwargs['eureka'] = eureka

        self.vote_object = eureka.comments.get(slug=kwargs['comment_slug'])
        return super(VoteUpEurekaCommentView, self).dispatch(request, *args, **kwargs)


class VoteUpConceptCommentView(VoteUpView):
    template_name = 'vote_concept_comment.html'

    def dispatch(self, request, *args, **kwargs):
        concept = get_object_or_404(Concept, slug=kwargs['slug'])
        kwargs['concept'] = concept

        self.vote_object = concept.comments.get(slug=kwargs['comment_slug'])
        return super(VoteUpConceptCommentView, self).dispatch(request, *args, **kwargs)


class VoteDownView(VoteActionView):
    def vote_action(self):
        self.was_voting = self.vote_object.votes.exists(self.request.user.id)
        if not self.was_voting:
            return

        self.was_voting = False
        self.vote_object.votes.delete(self.request.user.id)
        self.vote_object.created_by.rank.down()


class VoteDownEurekaView(VoteDownView):
    template_name = 'vote_eureka.html'

    def dispatch(self, request, *args, **kwargs):
        self.vote_object = get_object_or_404(Eureka, slug=kwargs['slug'])
        return super(VoteDownEurekaView, self).dispatch(request, *args, **kwargs)


class VoteDownConceptView(VoteDownView):
    template_name = 'vote_concept.html'

    def dispatch(self, request, *args, **kwargs):
        self.vote_object = get_object_or_404(Concept, slug=kwargs['slug'])
        return super(VoteDownConceptView, self).dispatch(request, *args, **kwargs)


class VoteDownEurekaLinkedView(VoteDownView):
    template_name = 'vote_eureka_linked.html'

    def dispatch(self, request, *args, **kwargs):
        eureka = get_object_or_404(Eureka, slug=kwargs['slug'])
        kwargs['eureka'] = eureka
        self.vote_object = eureka.links.get(slug=self.kwargs['linked_slug'])
        return super(VoteDownEurekaLinkedView, self).dispatch(request, *args, **kwargs)


class VoteDownConceptLinkedView(VoteDownView):
    template_name = 'vote_concept_linked.html'

    def dispatch(self, request, *args, **kwargs):
        concept = get_object_or_404(Concept, slug=kwargs['slug'])
        kwargs['concept'] = concept
        self.vote_object = concept.links.get(slug=self.kwargs['linked_slug'])
        return super(VoteDownConceptLinkedView, self).dispatch(request, *args, **kwargs)


class VoteDownEurekaCommentView(VoteDownView):
    template_name = 'vote_eureka_comment.html'

    def dispatch(self, request, *args, **kwargs):
        eureka = get_object_or_404(Eureka, slug=kwargs['slug'])
        kwargs['eureka'] = eureka
        self.vote_object = eureka.comments.get(slug=self.kwargs['comment_slug'])
        return super(VoteDownEurekaCommentView, self).dispatch(request, *args, **kwargs)


class VoteDownConceptCommentView(VoteDownView):
    template_name = 'vote_concept_comment.html'

    def dispatch(self, request, *args, **kwargs):
        concept = get_object_or_404(Concept, slug=kwargs['slug'])
        kwargs['concept'] = concept
        self.vote_object = concept.comments.get(slug=self.kwargs['comment_slug'])
        return super(VoteDownConceptCommentView, self).dispatch(request, *args, **kwargs)

