# -*- coding: UTF-8 -*-


# import sys
# import os


class Error(Exception):
    def __init__(self, message):
        self.message = message
        Exception.__init__(self, self.message)


class ObjectIdNotFound(Error):
    def __init__(self, object_id, model):
        Error.__init__(
            self, "[x] Object ID [%s] not found for given Model [%s]." % (
                object_id, model))


class NotWellFormatted(Error):
    def __init__(self, field_dict):
        Error.__init__(
            self, "[x] %s is not well formatted. Dictionary is expected." % (
                field_dict))


class FieldNotFound(Error):
    def __init__(self, field, model):
        Error.__init__(
            self, "[x] Field %s not found in given Model [%s]." % (
                field, model))


class ModelNotFound(Error):
    def __init__(self, model):
        Error.__init__(
            self, "[x] Model [%s] not found." % (model))


class NotExpectedModel(Error):
    """
        Error raised when model type is not expected.
    """
    def __init__(self, model):
        Error.__init__(
            self, "[x] Model [%s] have to be in str format." % (model))


class EmptyValue(Error):
    def __init__(self, model, field):
        Error.__init__(
            self, "[x] Field [%s] for [%s] have to be filled." % (field, model))
