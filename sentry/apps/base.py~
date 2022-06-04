#!/usr/bin/env python
# -*- coding: utf-8 -*-


from django.apps import AppConfig


class SentryConfig(AppConfig):
    name = "sentry"

    def ready(self):
        import sentry.signals.base
