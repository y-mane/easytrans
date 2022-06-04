#!/usr/bin/env python
# -*- coding: utf-8 -*-


import django
from datetime import datetime, timedelta
from django.conf import settings
from django.contrib.auth import logout
try: # Django 2.0
    from django.urls import reverse, resolve, Resolver404
except: # Django < 2.0
    from django.core.urlresolvers import reverse, resolve, Resolver404
from .utils import get_last_activity, set_last_activity


class SessionAutoLogout:

    def get_expire_seconds(self):
        """Return time (in seconds) before the user should be logged out."""
        return settings.SESSION_SECURITY_EXPIRE_AFTER

    def process_request(self, request):
        if django.VERSION < (1, 10):
            is_authenticated = request.user.is_authenticated()
        else:
            is_authenticated = request.user.is_authenticated

        # Can't log out if not logged in
        if not request.user.is_authenticated():
            return

        now = datetime.now()
        if '_session_security' not in request.session:
            set_last_activity(request.session, now)
            return

        delta = now - get_last_activity(request.session)
        expire_seconds = self.get_expire_seconds(request)
        last_activity = get_last_activity(request.session)

        if delta >= timedelta(seconds=expire_seconds):
            logout(request)
            del request.session['_session_security']
            return

        set_last_activity(request.session, last_activity)
