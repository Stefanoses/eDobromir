# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django_extensions.db.models import TimeStampedModel
from imagekit.models import ImageSpecField
from imagekit.processors import SmartResize


class ErrorReport(TimeStampedModel):
    actual_state = models.CharField(choices=(('Przetwarzanie', 'Przetwarzanie'),
                                             ('Naprawiono', 'Naprawiono'),
                                             ('Błędne zgłoszenie', 'Błędne zgłoszenie')),
                                    max_length=30, blank=True, verbose_name='Aktualny status', default='Przetwarzanie')
    comment_admin = models.TextField(verbose_name='Komentarz administratora', max_length=1000, blank=True)
    contact_email = models.EmailField(blank=True, verbose_name='Email kontaktowy (niewymagany)')
    error_login_state = models.CharField(choices=(('Zalogowany', 'Zalogowany'),
                                                  ('Niezalogowany', 'Niezalogowany'),
                                                  ('W obu przypadkach', 'W obu przypadkach'),
                                                  ('Nie dotyczy', 'Nie dotyczy')),
                                         verbose_name='Błąd występuje tylko wtedy kiedy jestem',
                                         max_length=30)
    error_code = models.CharField(choices=(('400', '400'),
                                           ('403', '403'),
                                           ('404', '404'),
                                           ('500', '500'),
                                           ('Całkowicie pusta strona', 'Całkowicie pusta strona'),
                                           ('Sam interfejs (menu, stopka)', 'Sam interfejs (menu, stopka)'),
                                           ('Ciągle ładująca się strona', 'Ciągle ładująca się strona'),
                                           ('Nie dotyczy', 'Nie dotyczy')),
                                  verbose_name='W czasie wystąpienia błędu pojawia się',
                                  max_length=30)
    error_type = models.CharField(choices=(('Nieszkodliwy', 'Nieszkodliwy'),
                                           ('Niebezpieczny', 'Niebezpieczny'),
                                           ('Krytyczny', 'Krytyczny')),
                                  verbose_name='Typ błędu',
                                  max_length=30)
    error_link = models.URLField(verbose_name='Błąd występuje na stronie (cały link wraz z https://www.)')
    error_description = models.TextField(verbose_name='Opis błędu', max_length=1000)
    error_image = models.ImageField(verbose_name='Zdjęcie (niewymagane)', upload_to='error_images', blank=True, null=True)