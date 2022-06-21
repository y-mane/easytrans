#!/usr/bin/env python
# -*- coding: utf-8 -*-


#  from django.conf.urls import url
from unicodedata import name
from django.urls import path
from django.conf.urls import include
from django.conf import settings
from django.conf.urls.static import static
from website.views import userspace as base
from oauth.urls import base as auth_urls
from website.views.payement_state import success,failled,notification
from .api import api

urlpatterns = [
    path('success/',success,name='success'),
    path('failled/',failled,name='failled'),
    path('notification/',notification,name='notification'),
    path('api/',api.urls)
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(
        settings.STATIC_URL, document_root=settings.STATIC_ROOT)
