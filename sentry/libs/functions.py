#!/usr/bin/python2.7
# -*- coding: UTF-8 -*-


from django.utils.translation import ugettext_lazy as _i18n
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User, Group
from django.utils.crypto import get_random_string
from django.http import HttpResponseForbidden
from django.core.mail import send_mail
from django.utils import translation
from django.conf import settings
from django.db.models import F
from django.db.models import Q

from sentry.models.base import *
from sentry.libs.errors import *

import os
import yaml
import json
import logging
import datetime
import xmltodict
import hashlib
import pyqrcode
import barcode
import requests
import _thread


logger = logging.getLogger('accesslog')
debug = logging.getLogger('debug')
log = logging.getLogger("sentry")

LOG_ENTRIES = [
    'CSRF_COOKIE', 'HTTP_COOKIE', 'HTTP_REFERER', 'HTTP_USER_AGENT',
    'HTTP_HOST', 'CONTENT_TYPE', 'REMOTE_ADDR', 'QUERY_STRING',
    'PATH_INFO', 'REQUEST_METHOD', 'REMOTE_HOST', 'SERVER_PORT',
    'CONTENT_LENGTH', 'HTTP_ACCEPT', 'HTTP_ACCEPT_ENCODING', 
    'HTTP_ACCEPT_LANGUAGE', 'REMOTE_USER', 'SERVER_NAME', 'HTTP_X_REAL_IP',
    'HTTP_X_FORWARDED_FOR', 'HTTP_X_FORWARDED_PROTO', 'HTTP_COOKIE'
]

# LANGUAGE = translation.get_language()
APP_TITLE = settings.APP_TITLE or _i18n('Sentry')
TICKETS_ADMIN = settings.TICKETS_ADMIN or 'support@mks-soft-technologies.com'
LANGUAGE = settings.LANGUAGE_CODE or 'fr'
EMAIL_HOST_USER = settings.EMAIL_HOST_USER or "no-reply@mks-soft-technologies.com"
PAAS_MICROSERVICES_BASE_SERVER = settings.PAAS_MICROSERVICES_BASE_SERVER or 'https://paas-notifications.com'
PAAS_MICROSERVICES_SEND_EMAIL = settings.PAAS_MICROSERVICES_SEND_EMAIL or '/emails/send/'
ALLOWED_HOSTS = settings.ALLOWED_HOSTS or list()

MODULE_DIR = os.path.dirname(os.path.dirname(__file__))
MODULE_CONFIG_DIR = os.path.join(MODULE_DIR, 'conf')
CURRENT_LANG_DIR = os.path.join(MODULE_CONFIG_DIR, LANGUAGE)
MESSAGES_FILE = os.path.join(CURRENT_LANG_DIR, 'messages.yaml')

with open(MESSAGES_FILE) as mf:
    messages = yaml.load(mf, Loader=yaml.SafeLoader)




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
def get_all_authorized_ips():
    return [_.source for _ in AuthorizedIPS.objects.all()]


def get_all_excluded_ips():
    return [_.source for _ in UnAuthorizedIPS.objects.all()]


# ------------------------------------------------------------------------------
# Setters
# ------------------------------------------------------------------------------
def set_action(data):
    return Action.objects.create(**data)


def set_cron_message(cron_job, message=str(), message_type='info'):
    try:
        CronJobMessage.objects.create(
            **{'cron_job': cron_job, 'message': message,
                'message_type': message_type})
    except Exception as e:
        log.error(f'[cron messaage] got error while setting cron message: {str(e)}')
        pass


def set_cron_job(name, ctype, description, start, end):
    cron = CronJob.objects.create(**{
        'name': name, 'description': description,
        'cron_type': ctype, 'start': start, 'end': end
    })
    set_cron_message(cron, f"Lancement cron: {name}")
    return True


# ------------------------------------------------------------------------------
# Updaters
# ------------------------------------------------------------------------------
# ------------------------------------------------------------------------------
# Actions
# ------------------------------------------------------------------------------
def record_history(data):
    """
        data contains:
        @params name: name of log history
        @params action_type: type of action, must be one of 'create', 'read',
            'update', 'delete'
        @params target: name of concerned class if present
        @params current_value: set in case of class objects log history
        @params new_value: set for value to log. in case of no class object,
            set for value to log
        @params description: description of log history
        @params owner: string of class:user(id) to display concerned by log
    """
    log.info("[history]: recording history ....")
    try:
        _thread.start_new_thread(set_action, (data,))
    except Exception as e:
        log.debug(f"[history] Encountered error during recording process: {str(e)}")
        send_emergency_mail(
            802, _i18n('Runtime Error'), {
                'app': APP_TITLE,
                'content': str(e),
                'location': 'recording history from logs module'
            })
        pass


def record_cron_job(name, ctype, description, start, end):
    try:
        _thread.start_new_thread(
            set_cron_job, (name, ctype, description, start, end))
    except Exception as e:
        log.debug(f"[cron job] Encountered error during recording process: {str(e)}")
        send_emergency_mail(
            802, _i18n('Runtime Error'), {
                'app': APP_TITLE,
                'content': str(e),
                'location': 'recording cron job from logs module'
            })
        pass


def send_emergency_mail(
        code, motive, datas=dict(), to=TICKETS_ADMIN,
        title=APP_TITLE, subject=_i18n('Runtime Error')):
    log.debug("[emergency]: Sending emergency Mail ...")
    message = messages[code].format(**datas)
    try:
        EmergencyMessage.objects.create(**{
            'code': code,
            'motive': motive,
            'message': message,
            'raw_data': str(datas),
            'title': title,
            'receiver': to,
        })
        send_mail(subject, message, EMAIL_HOST_USER, [to], fail_silently=True)
    except Exception as e:
        log.error("[emergency] failed to process emergency notification.")
        log.info("[emergency] attempting to send notification to admin through paas notifications ...")
        url = PAAS_MICROSERVICES_BASE_SERVER + PAAS_MICROSERVICES_SEND_EMAIL
        payload = {
            "title": _i18n('Runtime Error'),
            "motive": "Erreur envoi mails d'urgence",
            "to": "support@mks-soft-technologies.com",
            "content": "Une erreur est survenue lors de la tentative d'envoi de mails d'urgence.\nPriere de prendre le point en compte en urgence",
        }
        headers = {'content-type': 'application/x-www-form-urlencoded'}
        query = requests.post(url, data=payload, headers=headers)
        log.info(f"[+] emergency query ok ? {query.ok} ")
        log.info(f"[+] emergency query status code: {query.status_code}")
        log.info(f"[+] emergency query raw content: {query.content}")
        log.info(f"[+] emergency query result: {query.text}")
        pass


# ------------------------------------------------------------------------------
# Methods
# ------------------------------------------------------------------------------


# ------------------------------------------------------------------------------
# Decorators
# ------------------------------------------------------------------------------
def accesslog(function):
    """ get log of all META datas, username and user id """
    def wrap(request, *args, **kwargs):
        # retrieving intersection of LOG_ENTRIES and request.META.keys(),
        # in case of missing key, app will continue logging.
        webuser_id = request.user.id or 0
        # webuser_id = request.session.get('uid', 'Anonymous')
        webuser_name = request.user.username or 'anonymous'
        # webuser_name = request.session.get('uid', 'Anonymous')

        dict_data = {_: request.META[_] for _ in list(
            set(LOG_ENTRIES) & set(request.META.keys()))}
        log.info(
            "[ %s:%s:%s ]**[ function: %s ]**[ datas:%s ]" % (
                request.META['REMOTE_ADDR'], webuser_id, webuser_name,
                function.__name__, dict_data))
        return function(request, *args, **kwargs)
    return wrap


def inside(function):
    def wrap(request, *args, **kwargs):
        data_dict = {_: request.META[_] for _ in list(set(LOG_ENTRIES) & set(request.META.keys()))}
        logger.info("[=] Insider check for function handling ...")
        logger.info(f"[ function ]: {function.__name__} ##### [ datas ]: {data_dict}")
        if bool(is_in_allowed_hosts(request.META.get('HTTP_HOST', str()))):
            logger.info(f"[+] access granted to handle query for function: {function.__name__}")
            return function(request, *args, **kwargs)
        logger.info(f"[x] access denied to handle query for function: {function.__name__}")
        return HttpResponseForbidden(json.dumps("Forbidden Access"))
    return wrap


def whitelist(function):
    def wrap(request, *args, **kwargs):
        data_dict = {_: request.META[_] for _ in list(set(LOG_ENTRIES) & set(request.META.keys()))}
        logger.info("[=] Whitelist check for function handling ...")
        logger.info(f"[ function ]: {function.__name__} ##### [ datas ]: {data_dict}")
        if bool(
                is_in_remote_origins(request.META.get('REMOTE_ADDR', str())) or \
                    is_in_remote_origins(request.META.get('HTTP_X_FORWARDED_FOR', str())) or \
                    is_in_remote_origins(request.META.get('HTTP_X_REAL_IP', str()))):
            logger.info(f"[+] access granted to handle query for function: {function.__name__}")
            return function(request, *args, **kwargs)
        logger.info(f"[x] access denied to handle query for function: {function.__name__}")
        return HttpResponseForbidden(json.dumps("Forbidden Access"))
    return wrap


def blacklist(function):
    def wrap(request, *args, **kwargs):
        data_dict = {_: request.META[_] for _ in list(set(LOG_ENTRIES) & set(request.META.keys()))}
        logger.info("[=] Whitelist check for function handling ...")
        logger.info(f"[ function ]: {function.__name__} ##### [ datas ]: {data_dict}")
        if not bool(
                is_in_remote_excluded_origins(request.META.get('REMOTE_ADDR', str())) or \
                    is_in_remote_excluded_origins(request.META.get('HTTP_X_FORWARDED_FOR', str())) or \
                    is_in_remote_excluded_origins(request.META.get('HTTP_X_REAL_IP', str()))):
            logger.info(f"[+] access granted to handle query for function: {function.__name__}")
            return function(request, *args, **kwargs)
        logger.info(f"[x] access denied to handle query for function: {function.__name__}")
        return HttpResponseForbidden(json.dumps("Forbidden Access"))
    return wrap


def is_in_remote_origins(source):
    source_ips = source.split(',')
    allowed_source = get_all_authorized_ips()
    intersect_source_ip = list(set(source_ips).intersection(set(allowed_source)))
    if len(intersect_source_ip) > 0 or '*' in allowed_source:
        return True
    return False


def is_in_remote_excluded_origins(source):
    source_ips = source.split(',')
    excluded_source = get_all_excluded_ips()
    intersect_source_ip = list(set(source_ips).intersection(set(excluded_source)))
    if len(intersect_source_ip) > 0 or '*' in excluded_source:
        return True
    return False


def is_in_allowed_hosts(source):
    if source in ALLOWED_HOSTS or '*' in ALLOWED_HOSTS:
        return True
    return False


def check_app_system_status():
    log.info(f"[check_app_system_status] entering system check status ....")
    log.info(f"[check_app_system_status] trying to write something ....")
    record = AppCheck.objects.create(**{'content': 'Dummy text to write.'})
    log.info(f"[check_app_system_status] attempted to write in db to check system is full alive ...")
    log.info(f"[check_app_system_status] attempting to retrieve record ...")
    check = AppCheck.objects.all()
    log.info(f"[check_app_system_status] is record exists in db ? {check.exists()}")
    if not bool(check.exists()):
        log.info(f"[check_app_system_status] System need restart, system frozen ...")
        send_emergency_mail(
            802, 'Handing System health check',{
                'app': settings.APP_TITLE,
                'content': f'System frozen: System health check returned frozen system.',
                'location': '[root] check_app_system_status, System not working well, please restart quickly system ...'})
        return False

    else:
        check.delete()
        log.info(f"[check_app_system_status] Removing record, system not frozen !")
        log.info(f"[check_app_system_status] Everything is ok. Leaving ...")
    return True
