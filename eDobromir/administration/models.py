# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models


class BehaviorSettings(models.Model):
    eureka_main_page_point = models.PositiveIntegerField(verbose_name='Ilość punktów potrzebnych eurece na dostanie się na główna stronę.')
