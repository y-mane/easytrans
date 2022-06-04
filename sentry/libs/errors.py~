# -*- coding: UTF-8 -*-


import os
import yaml
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from django.utils import translation


# LANGUAGE = translation.get_language()
LANGUAGE = settings.LANGUAGE_CODE
MODULE_DIR = os.path.dirname(os.path.dirname(__file__))
MODULE_CONFIG_DIR = os.path.join(MODULE_DIR, 'conf')
CURRENT_LANG_DIR = os.path.join(MODULE_CONFIG_DIR, LANGUAGE)
MESSAGES_FILE = os.path.join(CURRENT_LANG_DIR, 'messages.yaml')

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


class NameNotProvided(Error):
    def __init__(self):
        Error.__init__(self, _(messages[904]))


class ContentNotProvided(Error):
    def __init__(self):
        Error.__init__(self, _(messages[905]))


class FormatNotRecognized(Error):
    def __init__(self):
        Error.__init__(self, _(messages[906]))


class SourceNotProvided(Error):
    def __init__(self):
        Error.__init__(self, _(messages[907]))


class NoDataProvided(Error):
    def __init__(self):
        Error.__init__(self, _(messages[908]))


class InvalidDateProvided(Error):
    def __init__(self):
        Error.__init__(self, _(messages[909]))


class MissingRequiredParams(Error):
    def __init__(self):
        Error.__init__(self, _(messages[904]))
