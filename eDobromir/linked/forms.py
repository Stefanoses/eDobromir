from django.forms import ModelForm
from .models import Linked

class LinkedCreateForm(ModelForm):
    class Meta:
        model = Linked
        fields = ['title', 'link']