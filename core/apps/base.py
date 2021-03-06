#!/usr/bin/env python
# -*- coding: utf-8 -*-


from django.apps import AppConfig


class BaseConfig(AppConfig):
    name = "core"

    def ready(self):
        import core.signals.base
