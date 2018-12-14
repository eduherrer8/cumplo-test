# -*- coding: utf-8 -*-
from django.views import View
from django.urls import reverse
from django.shortcuts import render
from django.urls import reverse_lazy
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic.edit import FormView

from cumplo_test_web.forms import RangeDates


class LandingView(View):
    """
    This view sends all unauthenticated users to login view
    """
    def get(self, request):
        """
        get method definition
        """
        if request.user.is_authenticated:
            return HttpResponseRedirect(reverse('web:dashboard'))
        return HttpResponseRedirect(reverse('web:auth:login'))


class AskDateRange(FormView):

    form_class = RangeDates
    template_name = "cumplo_test_web/info.html"

    def form_valid(self, form):
        return render(
            self.request, 'cumplo_test_web/results.html', data)
