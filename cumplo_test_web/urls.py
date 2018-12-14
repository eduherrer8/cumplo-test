# -*- coding: utf-8 -*-
from django.urls import path, include
from django.contrib.auth import views as auth_views

from . import views

app_name = "cumplo_test_web"

auth_patterns = ([
    path('login/',
         auth_views.LoginView.as_view(
            template_name='cumplo_test_web/accounts/login.html',
            redirect_authenticated_user=True),
         name='login'),
], 'auth')

urlpatterns = [
    path('accounts/', include(auth_patterns)),
    path('', views.LandingView.as_view(), name='index'),
    path('obtain-info/', views.AskDateRange.as_view(), name='dashboard'),
]
