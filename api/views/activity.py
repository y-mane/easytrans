#!/usr/bin/env python
# -*- coding: utf-8 -*-


from api.libs.functions import *
from api.serializers.activity import *

from rest_framework import viewsets
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view

from django.http import HttpResponseRedirect
from django.shortcuts import reverse

import datetime
import random
import json
import requests


@api_view(['GET'])
def group_perms(request, g=None):
    result = get_groups_permissions(g)
    return Response(result)


# -----------------------------------------------------------------------------
# Testings Purposes
# -----------------------------------------------------------------------------
