#!/usr/bin/env python
# -*- coding: utf-8 -*-


from django.db import models
from django.utils.crypto import get_random_string
from datetime import datetime
from django.utils.translation import ugettext_lazy as _
import uuid


class Base(models.Model):
    name = models.CharField(
        max_length=100, verbose_name=_("Name"), blank=True, db_index=True)
    internal_reference = models.UUIDField(
        max_length=15, verbose_name=_("Internal Reference"), default=uuid.uuid1,
        editable=False, db_index=True)
    reference = models.CharField(
        max_length=15, verbose_name=_("Reference"), blank=True, db_index=True)
    code = models.CharField(
        max_length=3, verbose_name=_("Code"), blank=True, db_index=True,
        editable=False
    )
    status = models.BooleanField(default=True, verbose_name=_("Status"))
    description = models.TextField(blank=True, verbose_name=_("Description"))
    created_at = models.DateField(
        auto_now=True, verbose_name=_("Created At"))
    updated_at = models.DateField(
        auto_now=False, verbose_name=_("Updated at"), null=True, blank=True,
        editable=False)

    def save(self, *args, **kwargs):
        if not self.reference:
            self.reference = get_random_string(length=15)
        if not self.name:
            self.name = self.reference
        self.updated_at = datetime.now()
        super(Base, self).save(*args, **kwargs)

    # def delete(self, *args, **kwargs):
        # # Overwrite classic delete to change only status
        # self.status = False
        # return self.id

    def __str__(self):
        return "%s" % self.name

    def __unicode__(self):
        return "%s" % self.name

    class Meta:
        abstract = True
