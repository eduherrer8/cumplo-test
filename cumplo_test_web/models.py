# -*- coding: utf-8 -*-
from django.db import models


class Series(models.Model):
    """
    This model will store the series information according to the banxico api
    """

    id_serie = models.CharField(max_length=60)
    title = models.TextField(blank=True)
    date_start = models.DateField()
    date_end = models.DateField()
    periodicity = models.CharField(blank=True, max_length=100)
    figure = models.CharField(blank=True, max_length=100)
    unit = models.CharField(blank=True, max_length=100)

    def __unicode__(self):
        return self.title


class ImageHelper(models.Model):
    image = models.ImageField(upload_to='figures/')
