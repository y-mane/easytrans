#!/usr/bin/env python
# -*- coding: utf-8 -*-


from django.db.models.signals import post_save
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.db.models import F
from oauth.models.base import *
#  from django.conf import settings
import logging
#  import os
#  import datetime


log = logging.getLogger("debug")


@receiver(post_save, sender=Branch)
def update_branches_count(sender, instance, created=False, **kwargs):
    log.info("[!] Got Branch post_save signal."
             "Attempting to get state (created value) ".format(created))
    log.info("[!] Got Branch post_save signal."
             "Attempting to get instance dict {}".format(instance.__dict__))

    if created:
        try:
            branches_count = ParamCountBranches.objects.get(id=1)
            branches_count.count = F('count') + 1
            branches_count.save()
            branches_count.refresh_from_db()
        except:
            ParamCountBranches.objects.create(**{'id': 1, 'count': 1})
