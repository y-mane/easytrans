#!/usr/bin/python2.7
# -*- coding: UTF-8 -*-


from django.contrib.auth.models import User, Group
from django.contrib.auth.hashers import make_password
from django.utils.translation import ugettext_lazy as _i18n
from django.conf import settings
from django.core.mail import send_mail
from django.utils.crypto import get_random_string
from django.utils import translation
from django.db.models import F
#  from django.db.models import Count
#  from django.db import transaction
#  from django.db.models import Q

from oauth.models.base import *

import yaml
import json
from .errors import *
import logging
import datetime
import xmltodict
import os
import hashlib
import pyqrcode
import barcode
import requests
import _thread


LANGUAGE = translation.get_language()
CURRENT_LANG_DIR = os.path.join(settings.CONFIG_DIR, LANGUAGE)
MESSAGES_FILE = os.path.join(CURRENT_LANG_DIR, settings.MESSAGES_FILE)

with open(MESSAGES_FILE) as mf:
    messages = yaml.load(mf, Loader=yaml.SafeLoader)


default_log = logging.getLogger("default")
debug_log = logging.getLogger("debug")
log = logging.getLogger("request")
plog = logging.getLogger("request")


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
def get_forms_choices(model):
    """
        Function to retrieve id and name of records of model to make as tuple
        for setting choices in forms.ChoiceField to validate forms
    """
    check_instance(model)
    if model == "User":
        return [(_.id, _.username) for _ in eval(
            model).objects.all()]
    data = [(_.id, _.name) for _ in eval(model).objects.filter(status=True)]
    return data


def get_user_lang(user_id):
    default_lang = 'fr'
    user = User.objects.get(id=user_id)
    try:
        user_lang = UserLang.objects.get(user=user)
        default_lang = user_lang.lang
    except:
        debug_log.debug("[x] User hasn't default_lang set. Will use default")
        pass
    return default_lang


def get_forms_choices_for_user(model, user_id):
    check_instance(model)
    user = User.objects.get(id=user_id)
    data = [(_.id, _.name) for _ in eval(model).objects.filter(
        status=True).filter(owner=user)]
    return data


def get_model_data(model, filter_params=dict(), order='id', limit=50, id=None):
    """
        Function to get data no matter given model
        :param model: str, model tousse to get data
        :param id: int, id of single record
    """
    check_instance(model)
    if id is not None:
        return eval(model).objects.get(id=id)
    cleaned_filter_params = clean_query_params(model, filter_params)
    return eval(model).objects.filter(**cleaned_filter_params).order_by(
        order)[:limit]


def get_model_paginator(model, filter_params=dict()):
    """
        Function to get data for paginator function
        :param model: str, model to use to get data
        :param filter_params: dict, parameters for filtering records
    """
    check_instance(model)
    cleaned_filter_params = clean_query_params(model, filter_params)
    return eval(model).objects.filter(**cleaned_filter_params)


def get_model_data_for_owner(model, filter_params=dict(), order='id',
                             limit=50, owner_id=None):
    """
        Function to get data no matter given model
        :param model: str, model where to get data
        :param id: int, id of single record
    """
    check_instance(model)
    cleaned_filter_params = clean_query_params(model, filter_params)
    if owner_id is not None:
        owner = User.objects.get(id=owner_id)
        return eval(model).objects.filter(owner=owner).filter(
            **cleaned_filter_params).order_by(order)[:limit]
    return eval(model).objects.filter(**cleaned_filter_params).order_by(
        order)[:limit]


def get_single_record(model, id):
    check_instance(model)
    return eval(model).objects.get(id=id)


def get_model_records(model, ids):
    check_instance(model)
    return eval(model).objects.filter(id__in=ids)


def get_user_profile(user):
    return Profile.objects.get(user=user)


def get_day_from_date(date):
    year, month, day = [int(_) for _ in date.split("-")]
    return datetime.date(year, month, day).strftime("%A").lower()


def get_date_from_str(str_date):
    year, month, day = [int(_) for _ in str_date.split("-")]
    return datetime.date(year, month, day)


def get_app_users():
    data = list()
    # users = User.objects.filter(is_superuser=False).filter(is_active=True)
    users = User.objects.filter(is_superuser=False)
    for _ in users:
        data.append(
            {
                'user': _,
                'groups': [g.name for g in _.groups.all()][0],
                'profile': Profile.objects.filter(user=_)
            }
        )
    return data


def get_app_user_message(user_id, code):
    LANGUAGE = get_user_lang(user_id)
    CURRENT_LANG_DIR = os.path.join(settings.CONFIG_DIR, LANGUAGE)
    MESSAGES_FILE = os.path.join(CURRENT_LANG_DIR, settings.MESSAGES_FILE)

    with open(MESSAGES_FILE) as mf:
        messages = yaml.load(mf, Loader=yaml.SafeLoader)
    return messages


def get_notification_content(user_id, code, kwargs=dict()):
    LANGUAGE = get_user_lang(user_id)
    CURRENT_LANG_DIR = os.path.join(settings.CONFIG_DIR, LANGUAGE)
    MESSAGES_FILE = os.path.join(CURRENT_LANG_DIR, settings.MESSAGES_FILE)

    with open(MESSAGES_FILE) as mf:
        messages = yaml.load(mf, Loader=yaml.SafeLoader)
    return messages[code].format(**kwargs)


def get_branch_count():
    return Branch.objects.count()


def get_all_users_of_group(group_name, exclude_users=None):
    if bool(exclude_users):
        return User.objects.filter(
            groups__name=group_name).exclude(id__in=exclude_users)
    return User.objects.filter(groups__name=group_name)


def get_all_profile_of_group(group_name, exclude_users=None):
    tmp = list()
    if bool(exclude_users):
        tmp = User.objects.filter(
            groups__name=group_name).exclude(id__in=exclude_users)
    else:
        tmp = User.objects.filter(groups__name=group_name)

    return Profile.objects.filter(user__in=tmp)


# ------------------------------------------------------------------------------
# Setters
# ------------------------------------------------------------------------------
def handle_mail_sending(message, to, motive=_i18n('Gestion Utilisateurs')):
    debug_log.debug("[+] Sending Mail: %s" % message)
    return send_mail(
        "[%s]: %s" % (settings.APP_TITLE, motive),
        message, settings.EMAIL_HOST_USER, [to], fail_silently=True
    )


# ------------------------------------------------------------------------------
# Updaters
# ------------------------------------------------------------------------------
# ------------------------------------------------------------------------------
# Actions
# ------------------------------------------------------------------------------
def generate_barcode_image(barcode_name, barcode_data, barcode_type='code128',
                           barcode_format='.png',
                           default_path=settings.BARCODE_ROOT):
    #  barcode_image = treepoem.generate_barcode(
    #      barcode_type=barcode_type,
    #      data=barcode_data,
    #  )
    #  barcode_image.convert('1').save(os.path.join(default_path, "%s%s" % (
    #      barcode_name, barcode_format)))
    barcode.generate(barcode_type, barcode_data, output=os.path.join(
        default_path, "%s" % barcode_name))


def generate_qrcode_image(qrcode_name, qrcode_data,
                          default_path=settings.BARCODE_ROOT):
    qr = pyqrcode.create(qrcode_data)
    log.debug("[!] Qr: {}".format(qr))
    qr.svg(os.path.join(default_path, "%s.svg" % qrcode_name), scale=8)


def check_number_length(str_number, length):
    return len(str_number) == length


def sendsms(message, to):
    url = "https://mks-microservices.tech/sms/send/"
    payload = {'_to': to, 'message': message}
    debug_log.debug(
        "[+] Requesting SMS Server for sending: {}".format(payload))
    query = requests.post(url, data=payload)
    return query.text


# ------------------------------------------------------------------------------
# Methods
# ------------------------------------------------------------------------------
def check_instance(model):
    """
        Checks if given model is a string. String model will be evaluated
        before each operation.
        we can get all data for model in _meta dict
    """
    if not isinstance(model, str):
        raise NotExpectedModel(model)
    try:
        eval(model)._meta.label_lower
        debug_log.debug('[!] function: check_instance. Got {}.' +
                        ' Attempting to get metadata of given model: {}'.format(
                            model, {k: v for k, v in
                                    eval(model)._meta.__dict__.items()}))
    except Exception as e:
        debug_log.debug("[x] Got Exception: {}".format(str(e)))
        raise ModelNotFound(model)


def clean_query_params(model, query_params):
    result = dict(query_params)
    default_log.info("[!] Starting with query_params: {} in model: {}".format(
        query_params, model))
    model_fields = [_.name for _ in eval(model)._meta.get_fields()]
    for _ in query_params.keys():
        if _ not in model_fields:
            default_log.info("[x] {} is not in model: {} fields. " +
                             "Removing it".format(_, model))
            del result[_]
    return result


def clean_dict(args):
    result = dict(args)
    for _ in args.keys():
        if not bool(args[_]):
            del result[_]
    return result


def format_time_AM_PM(str_time):
    period = str_time[-2:]
    hours, mins = int(
        str_time[:-2].split(":")[0]), int(str_time[:-2].split(":")[1])
    if period == 'PM':
        hours += 12
    return "%s:%s" % (hours, mins)


def format_time(str_time):
    hours, mins = int(str_time.split(":")[0]), int(str_time.split(":")[1])
    return datetime.time(hours, mins)


def format_name_string(string):
    return string.replace(' ', '.').replace('\'', '').replace('"', '')


def format_num(num):
    return "".join(num.split(" "))


def format_number_for_sms_send(str_number):
    return "225%s" % format_num(str_number)


def format_date_time(date_time_obj):
    return date_time_obj.strftime("%d/%m/%Y - %H:%M")


def get_zfill_data(data, width):
    return "{data}".format(data=data).zfill(width)


def isExists(model, params_dict):
    return eval(model).objects.filter(**params_dict).exists()
