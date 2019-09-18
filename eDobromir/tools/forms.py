from django import forms
from tools.models import IpStampedModel
from ipware.ip import get_ip

class IpStampedForm(forms.ModelForm):
    class Meta:
        model = IpStampedModel


    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(IpStampedForm, self).__init__(*args, **kwargs)

    def save(self, commit=True):
        instance = super(IpStampedForm, self).save(commit=False)
        instance.ip_adress = get_ip(self.request)

        if commit:
            instance.save()

        return instance