from __future__ import unicode_literals

from django.db import models
from ipware.ip import get_ip

class IpStampedModel(models.Model):
    ip_adress = models.GenericIPAddressField()

    class Meta:
        abstract = True