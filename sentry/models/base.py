#!/usr/bin/env python
# -*- coding: utf-8 -*-


from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext as _
import uuid


class Action(models.Model):
    name = models.CharField(max_length=100, verbose_name=_("Libellé"), blank=True)
    reference = models.UUIDField(
        max_length=15, verbose_name=_("Réference Interne"), default=uuid.uuid1,
        editable=False)
    status = models.BooleanField(default=True, verbose_name=_("Status"),
        editable=False)
    action_type = models.CharField(
        max_length=100, verbose_name=_("Libellé"),
        choices=[
            ('create', _('Création')), ('read', _('Lecture')),
            ('update', _('Mise à Jour')), ('delete', _('Suppression'))],
        default='read')
    target = models.CharField(
        max_length=200, verbose_name=_("Cible"), default=_('all'))
    current_value = models.TextField(
        verbose_name=_("Valeur Courante"), blank=True, null=True)
    new_value = models.TextField(
        verbose_name=_("Nouvelle Valeur"), blank=True, null=True)
    record_class = models.CharField(max_length=150, verbose_name=_("Classe"))
    description = models.TextField(blank=True, verbose_name=_("Description"))
    owner = models.TextField(blank=True, verbose_name=_("Owner"), editable=False, null=True)
    created_at = models.DateTimeField(
        auto_now=True, editable=False, verbose_name=_('Date Création'))

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.name:
            self.name = self.reference
        super(Action, self).save(*args, **kwargs)

    class Meta:
        ordering = ('-id',)


class CronJob(models.Model):
    name = models.CharField(
        max_length=200, verbose_name=_('Libelle'), null=True,
        blank=True, editable=False)
    reference = models.UUIDField(
        max_length=15, verbose_name=_("Réference Interne"), default=uuid.uuid1,
        editable=False, db_index=True)
    created_at = models.DateField(
        auto_now=True, editable=False, verbose_name=_('Date Création'))
    start = models.DateTimeField(
        auto_now=False, editable=False, verbose_name=_('Date Début'),
        null=True, blank=True)
    end = models.DateTimeField(
        auto_now=False, editable=False, verbose_name=_('Date Fin'),
        null=True, blank=True)
    cron_type = models.CharField(
        max_length=200, verbose_name=_('Type Cron'), null=True,
        blank=True, editable=False)
    description = models.TextField(
        verbose_name=_("Description"), blank=True, editable=False, null=True) 

    def __str__(self):
        return "%s" % self.reference

    class Meta:
        verbose_name = _('Cron')
        ordering = ('-id',)


class CronJobMessage(models.Model):
    reference = models.UUIDField(
        max_length=15, verbose_name=_("Réference Interne"), default=uuid.uuid1,
        editable=False, db_index=True)
    created_at = models.DateTimeField(
        auto_now=True, editable=False, verbose_name=_('Date Message'))
    cron_job = models.ForeignKey(
        CronJob, verbose_name=_('Cron'),
        on_delete=models.SET_NULL, null=True, blank=True, editable=False)
    message = models.TextField(
        verbose_name=_("Message"), blank=True, editable=False) 
    message_type = models.CharField(
        max_length=20, verbose_name=_('Type Message'),
        choices=[
            ('info', _('Infos')), ('error', _('Erreur')),
            ('debug', _('Débogage'))], default='info', editable=False)

    def __str__(self):
        return "%s" % self.reference

    class Meta:
        verbose_name = _('Message Cron')
        verbose_name_plural = _('Messages Crons')
        ordering = ('-id',)


class EmergencyMessage(models.Model):
    reference = models.UUIDField(
        max_length=15, verbose_name=_("Réference Interne"), default=uuid.uuid1,
        editable=False)
    created_at = models.DateTimeField(
        auto_now=True, editable=False, verbose_name=_('Date Message'))
    code = models.CharField(
        max_length=20, null=True, blank=True, verbose_name=_('Code'), editable=False)
    motive = models.TextField(
        verbose_name=_("Motif"), blank=True, editable=False) 
    message = models.TextField(
        verbose_name=_("Message"), blank=True, editable=False) 
    raw_data = models.TextField(
        verbose_name=_("Raw Datas"), blank=True, editable=False) 
    title = models.TextField(
        verbose_name=_("Titre"), blank=True, editable=False) 
    receiver = models.CharField(
        max_length=200, null=True, blank=True, verbose_name=_('Destinataire'), editable=False)

    def __str__(self):
        return "%s" % self.reference

    class Meta:
        verbose_name = _('Message Urgence')
        verbose_name_plural = _('Messages Urgences')
        ordering = ('-id',)


class AuthorizedIPS(models.Model):
    name = models.CharField(max_length=200, blank=True, verbose_name=_("Libelle"))
    source = models.CharField(max_length=150, blank=True, verbose_name=_("Source"))
    description = models.TextField(blank=True, verbose_name=_("Description"))
    status = models.BooleanField(default=True, verbose_name=_("Statut"))
    created_at = models.DateTimeField(
        auto_now=True, editable=False, verbose_name=_('Création'))

    def __str__(self):
        return "%s" % self.source

    class Meta:
        verbose_name = _('IPs Autorisées')
        verbose_name_plural = _('IPs Autorisées')
        ordering = ('source',)


class UnAuthorizedIPS(models.Model):
    name = models.CharField(max_length=200, blank=True, verbose_name=_("Libelle"))
    source = models.CharField(max_length=150, blank=True, verbose_name=_("Source"))
    description = models.TextField(blank=True, verbose_name=_("Description"))
    status = models.BooleanField(default=True, verbose_name=_("Statut"))
    created_at = models.DateTimeField(
        auto_now=True, editable=False, verbose_name=_('Création'))

    def __str__(self):
        return "%s" % self.source

    class Meta:
        verbose_name = _('IPs Exclues')
        verbose_name_plural = _('IPs Exclues')
        ordering = ('source',)


class AppCheck(models.Model):
    created = models.DateTimeField(auto_now=True)
    content = models.CharField(max_length=250, blank=True, null=True)
