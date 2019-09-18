# -*- coding: utf-8 -*-
from django.forms import ModelForm, ChoiceField, RadioSelect
from .models import Moderation

class ReportModerationForm(ModelForm):
    choices = (
        ('Treść pornograficzna', 'Treść pornograficzna'),
        ('Oszustwo, wprowadza w błąd', 'Oszustwo, wprowadza w błąd'),
        ('Propagowanie nienawiści', 'Propagowanie nienawiści'),
        ('Reklama, spam', 'Reklama, spam'),
        ('Atakowanie, oczernianie', 'Atakowanie, oczernianie'),
        ('Narusza regulamin strony', 'Narusza regulamin strony'),
        ('Niepoprawne tagi', 'Niepoprawne tagi'),
        ('Manipulacja głosami', 'Manipulacja głosami'),
        ('Nie nadaje się', 'Nie nadaje się'),
        ('Duplikat', 'Duplikat'),
        ('Informacje nieprawdiwe', 'Informacje nieprawdiwe'),
        ('Treść nieodpowiednia', 'Treść nieodpowiednia'),
        ('Inne', 'Inne'),
    )

    choiceReason = ChoiceField(widget=RadioSelect, choices=choices, label='Powód')

    class Meta:
        model = Moderation
        fields = ['choiceReason', 'reason']