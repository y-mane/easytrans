#!/usr/bin/env python
# -*- coding: utf-8 -*-


from django.db.models.signals import post_save
#  from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.db.models import F
from oauth.models.base import *
#  from django.conf import settings
import logging
#  import os
#  import datetime


log = logging.getLogger("debug")
