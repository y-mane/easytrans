#!/usr/bin/env python
# -*- coding: utf-8 -*-


from django.apps import AppConfig


class BaseOAuthConfig(AppConfig):
    name = "oauth"

    def ready(self):
        import oauth.signals.base
