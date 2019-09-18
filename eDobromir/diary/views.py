from django.shortcuts import render
from django.views.generic import DetailView
from .models import Diary


class DiaryOpenView(DetailView):
    def dispatch(self, request, *args, **kwargs):
        super(DiaryOpenView, self).dispatch(request, *args, **kwargs)

        if not request.session.session_key:
            request.session.create()
        if not self.object.diarys.filter(session=request.session.session_key):
            self.object.diarys.create(ip=request.META['REMOTE_ADDR'],
                                        session=request.session.session_key)

        return super(DiaryOpenView, self).dispatch(request, *args, **kwargs)
