#!/usr/bin/env python
# -*- coding: utf-8 -*-


from sentry.libs.errors import *
from sentry.libs.functions import *

from rest_framework import viewsets
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view

from django.utils.translation import ugettext_lazy as _
from django.utils import translation
from django.conf import settings
from django.core.paginator import Paginator

import logging
import requests


log = logging.getLogger('sentry')


# LANGUAGE = translation.get_language()
LANGUAGE = settings.LANGUAGE_CODE
MODULE_DIR = os.path.dirname(os.path.dirname(__file__))
MODULE_CONFIG_DIR = os.path.join(MODULE_DIR, 'conf')
CURRENT_LANG_DIR = os.path.join(MODULE_CONFIG_DIR, LANGUAGE)
MESSAGES_FILE = os.path.join(CURRENT_LANG_DIR, 'messages.yaml')

with open(MESSAGES_FILE) as mf:
    messages = yaml.load(mf, Loader=yaml.SafeLoader)


# -----------------------------------------------------------------------------
# GET Functions
# -----------------------------------------------------------------------------
@accesslog
@api_view(['GET'])
def handle_system_check_alive(request):
    result = False
    message = 0
    status_to_return = status.HTTP_400_BAD_REQUEST
    state = 'error'

    try:
        result = True
        message = 700
        state = 'success'
        status_to_return = status.HTTP_200_OK

    except Exception as e:
        log.error(f"[handle_system_check_alive] got error while processing query: {str(e)}")
        message = 712

    data_to_return = {
        'result': result, 'state': state, 'message': messages[message]}
    log.debug(f"[=] Data to return for #handle_system_check_alive: {data_to_return}")
    return Response(data_to_return, status=status_to_return)


@accesslog
@api_view(['GET'])
def handle_system_check_status(request):
    result = False
    message = 0
    status_to_return = status.HTTP_400_BAD_REQUEST
    state = 'error'

    try:
        log.info(f"[handle_system_check_status] handling system status check ...")
        result = check_app_system_status()
        message = 700
        state = 'success'
        status_to_return = status.HTTP_200_OK

    except Exception as e:
        log.error(f"[handle_system_check_status] got error while processing query: {str(e)}")
        message = 712
        send_emergency_mail(
            802, 'Handing app check system status',{
                'app': settings.APP_TITLE,
                'content': f'Error encountered: {str(e)}',
                'location': 'handle_system_check_status'})
        pass

    data_to_return = {
        'result': result, 'state': state, 'message': messages[message]}
    return Response(data_to_return, status=status_to_return)



# -----------------------------------------------------------------------------
# POST Functions
# -----------------------------------------------------------------------------
# -----------------------------------------------------------------------------
# PUT Functions
# -----------------------------------------------------------------------------
# -----------------------------------------------------------------------------
# HEAD Functions
# -----------------------------------------------------------------------------
# -----------------------------------------------------------------------------
# DELETE Functions
# -----------------------------------------------------------------------------
