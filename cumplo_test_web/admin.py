# -*- coding: utf-8 -*-
from django.contrib import admin
from cumplo_test_web.models import Series


class SeriesAdmin(admin.ModelAdmin):
    list_display = ('id_serie', 'date_start', 'date_end',)
    ordering = ('pk',)


admin.site.register(Series, SeriesAdmin)
