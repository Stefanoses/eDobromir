from django.shortcuts import render
from ratelimit.mixins import RatelimitMixin
from ratelimit.utils import is_ratelimited
from ratelimit.decorators import ratelimit
from django.contrib import messages
from django.views.generic.base import View, TemplateView
from ratelimit.exceptions import Ratelimited

class RatelimitUserOrIpView(RatelimitMixin):
    ratelimit_key = 'user_or_ip'
    ratelimit_rate = '1/20s'
    ratelimit_block = True


class RatelimitEurekaCreateView(RatelimitUserOrIpView):
    ratelimit_rate = '1/20s'


class RatelimitEurekaStepCreateView(RatelimitUserOrIpView):
    ratelimit_rate = '1/20s'


class RatelimitConceptCreateView(RatelimitUserOrIpView):
    ratelimit_rate = '1/20s'


class RatelimitCommentsCreateView(RatelimitUserOrIpView):
    ratelimit_rate = '1/20s'


class RatelimitCommentsReplyView(RatelimitUserOrIpView):
    ratelimit_rate = '1/20s'


class RatelimitContentErrorReportCreateView(RatelimitUserOrIpView):
    ratelimit_rate = '1/60s'


class RatelimitContentContactView(RatelimitUserOrIpView):
    ratelimit_rate = '1/20s'


class RatelimitLinkedCreateView(RatelimitUserOrIpView):
    ratelimit_rate = '1/20s'


class RatelimitVoteActionView(RatelimitUserOrIpView):
    ratelimit_rate = '1/3s'

class RatelimitConversationCreateView(RatelimitUserOrIpView):
    ratelimit_rate = '1/5s'