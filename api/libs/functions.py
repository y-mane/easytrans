#!/usr/bin/python2.7
# -*- coding: UTF-8 -*-

from django.contrib.auth.models import Group, User, Permission, ContentType

from .errors import NotExpectedModel
from .errors import ModelNotFound

from oauth.models.base import Profile, UserboardPermission

import json
import datetime
import logging


log = logging.getLogger("api")


# All functions for CRUD. functions are structured accroding theirs work
# action[_quantity]_type[_by_criteria]
# ex: get_all_client_by_id, set_client_by_username, get_all_mode, get_user_by_id
# functions return list called result
# ##############################################################################
#
#
# ------------------------------------------------------------------------------
# Getters
# ------------------------------------------------------------------------------
def get_model_data(model, id=None):
    """
        Function to get data no matter given model
        :param model: str, model tousse to get data
        :param id: int, id of single record
    """
    check_instance(model)
    if id is not None:
        return eval(model).objects.get(id=id)
    return eval(model).objects.all()


def get_user_branch_v2(user):
    profile = Profile.objects.get(user=user)
    return profile.branch


def get_groups_permissions(group=None):
    data = list()
    all_groups = [_.name for _ in Group.objects.all()]
    if bool(group):
        uperms = UserboardPermission()
        data = uperms.get_group_permissions(group)
    else:
        contentype = ContentType.objects.get_for_model(UserboardPermission)
        data = [
            (_.codename, _.name) for _ in Permission.objects.filter(
                content_type=contentype)]
    return data


# ------------------------------------------------------------------------------
# Setters
# ------------------------------------------------------------------------------
def change_status(model, field, status=True, id=None):
    """
        Function to change status of given boolean field no matter given model
        :param model: str, model to get data
        :param id: int, id of single record
        :param field: str, boolean field to change status
        :param status: bool, default status to assign
    """
    check_instance(model)
    data = {field: status}
    if id is not None:
        return eval(model).objects.filter(id=id).update(**data)
    return eval(model).objects.update(**data)


# ------------------------------------------------------------------------------
# Updaters
# ------------------------------------------------------------------------------
# ------------------------------------------------------------------------------
# Actions
# ------------------------------------------------------------------------------
def get_city_branches(city_id):
    city = City.objects.get(id=city_id)
    data = [(_.id, _.name) for _ in Branch.objects.filter(city=city)]
    return json.dumps(data)


# ------------------------------------------------------------------------------
# Methods
# ------------------------------------------------------------------------------
def check_instance(model):
    """
        Checks if given model is a string. String model will be evaluated
        before each operation.
    """
    if not isinstance(model, str):
        raise NotExpectedModel(model)
    try:
        eval(model)._meta.label_lower
    except NameError:
        raise ModelNotFound(model)
