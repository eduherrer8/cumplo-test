# -*- coding: utf-8 -*-
"""
"""
from django import forms
from django.utils import timezone


class RangeDates(forms.Form):
    """
    """
    date_start = forms.DateField()
    date_end = forms.DateField()

    def clean_date_end(self):
        date = self.cleaned_data.get('date_end')
        if date and date > timezone.now().date():
            self.add_error('date_end', "no puede ser menor a hoy")
        return date

    def clean(self):
        cleaned_data = super().clean()
        date_start = cleaned_data.get("date_start")
        date_end = cleaned_data.get("date_end")
        if date_end < date_start:
            self.add_error('date_start', "no puede ser menor")
