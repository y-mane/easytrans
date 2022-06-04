# -*- coding: UTF-8 -*-


# import sys
import os
import yaml
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from django.utils import translation


LANGUAGE = translation.get_language()
CURRENT_LANG_DIR = os.path.join(settings.CONFIG_DIR, LANGUAGE)
MESSAGES_FILE = os.path.join(CURRENT_LANG_DIR, settings.MESSAGES_FILE)


with open(MESSAGES_FILE) as mf:
    messages = yaml.load(mf, Loader=yaml.SafeLoader)


class Error(Exception):
    def __init__(self, message):
        self.message = message
        Exception.__init__(self, self.message)


class NotWellFormatted(Error):
    def __init__(self, field_dict):
        Error.__init__(
            self, _(messages[900].format(args=field_dict)))


class FieldNotFound(Error):
    def __init__(self, field, model):
        Error.__init__(
            self, _(messages[901].format(
                field=field, model=model)))


class ModelNotFound(Error):
    def __init__(self, model):
        Error.__init__(
            self, _(messages[902].format(model=model)))


class NotExpectedModel(Error):
    def __init__(self, model):
        Error.__init__(
            self, _(messages[903].format(model=model)))
