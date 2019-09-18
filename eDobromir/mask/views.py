from django.shortcuts import render
from django.views.generic.edit import FormView
from mask.models import DeleteMask


class CreateDeleteMaskView(FormView):
    def form_valid(self, form):
        form.instance.delete_mask = DeleteMask.objects.create()
        return super(CreateDeleteMaskView, self).form_valid(form)