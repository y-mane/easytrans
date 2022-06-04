#!/usr/bin/env python
# -*- coding: utf-8 -*-


from django.urls import path
from sentry.views.base import *


urlpatterns = [
    path("check-system-alive/", handle_system_check_alive, name="system_check_alive"),
    path("check-system-status/", handle_system_check_status, name="system_check_status"),
]
