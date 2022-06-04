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
from website.views.frontspace import frontspace
from website.views.frontspace import load_agence,load_destination


urlpatterns = [
    path('',frontspace,name='frontspace'),
    path('ajax/load-lieu_depart/',load_agence,name="ajax_load_lieu_depart"),
    path('ajax/load-destination/',load_destination,name="ajax_load_destination"),

]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(
        settings.STATIC_URL, document_root=settings.STATIC_ROOT)
