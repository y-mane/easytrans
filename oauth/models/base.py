#!/usr/bin/env python
# -*- coding: utf-8 -*-


from django.db import models
from django.contrib.auth.models import User, Group, ContentType, Permission
from django.utils.translation import ugettext_lazy as _
from django.utils.crypto import get_random_string
#  from django.core.validators import MinValueValidator
from django.db.models.signals import post_save
from django.dispatch import receiver

#  import os
import uuid
import datetime
#  import pyqrcode
#  from decimal import Decimal


# -------------------- Base Abstract Model ------------------------------------
class Base(models.Model):
    name = models.CharField(
        max_length=100, verbose_name=_("Libellé"), blank=True, db_index=True)
    internal_reference = models.UUIDField(
        max_length=15, verbose_name=_("Référence Interne"), default=uuid.uuid1,
        editable=False, db_index=True)
    reference = models.CharField(
        max_length=6, verbose_name=_("Réference"), blank=True, db_index=True)
    code = models.CharField(
        max_length=3, verbose_name=_("Code"), blank=True, db_index=True,
        editable=False
    )
    status = models.BooleanField(default=True, verbose_name=_("Statut"))
    description = models.TextField(blank=True, verbose_name=_("Description"))
    created_at = models.DateField(
        auto_now=True, verbose_name=_("Création"))
    updated_at = models.DateField(
        auto_now=False, verbose_name=_("Mise à jour"), null=True, blank=True,
        editable=False)

    def save(self, *args, **kwargs):
        if not self.reference:
            self.reference = get_random_string(length=6)
        if not self.name:
            self.name = self.reference
        self.updated_at = datetime.datetime.now()
        super(Base, self).save(*args, **kwargs)

    def __str__(self):
        return "%s" % self.name

    def __unicode__(self):
        return "%s" % self.name

    class Meta:
        abstract = True
# -----------------------------------------------------------------------------


class UserLang(models.Model):
    user = models.ForeignKey(
        User, verbose_name=_("Utilisateur"), on_delete=models.DO_NOTHING, null=True)
    lang = models.CharField(
        max_length=50, blank=True, verbose_name=_("Langue Utilisateur"),
        choices=[
            ('en', _('Anglais')), ('fr', _('Français'))
        ], default='fr')

    def __str__(self):
        return "%s - %s" % (self.user, self.lang)

    class Meta:
        verbose_name = _("Langue Utilisateur")
        verbose_name_plural = _("Langues Utilisateurs")


class UserRecover(models.Model):
    user = models.ForeignKey(
        User, verbose_name=_("Utilisateur"), on_delete=models.DO_NOTHING, null=True)
    recover_code = models.CharField(verbose_name=_(
        "Code Récupération"), max_length=10, blank=True, null=True)

    def __str__(self):
        return "%s - %s" % (self.user, self.recover_code)

    class Meta:
        verbose_name = _("Code Récupération")
        verbose_name_plural = _("Codes Récupérations")


class Signature(models.Model):
    sig = models.CharField(max_length=255, blank=True)


class City(models.Model):
    name = models.CharField(
        max_length=100, verbose_name=_("Libellé"), blank=True)
    reference = models.CharField(
        max_length=30, verbose_name=_("Réference"), blank=True, db_index=True)
    description = models.TextField(blank=True, verbose_name=_("Description"))
    status = models.BooleanField(default=True, verbose_name=_("Statut"))

    def __str__(self):
        return "%s" % self.name

    class Meta:
        verbose_name = _("Ville")


class Town(models.Model):
    name = models.CharField(
        max_length=100, verbose_name=_("Libellé"), blank=True)
    reference = models.CharField(
        max_length=30, verbose_name=_("Réference"), blank=True, db_index=True)
    description = models.TextField(blank=True, verbose_name=_("Description"))
    city = models.ForeignKey(
        City, verbose_name=_('Ville'), on_delete=models.DO_NOTHING)
    status = models.BooleanField(default=True, verbose_name=_("Statut"))

    def __str__(self):
        return "%s" % self.name

    class Meta:
        verbose_name = _("Quartier / Commune")
        verbose_name_plural = _("Quartiers / Communes")


class Branch(Base):
    phone = models.CharField(
        max_length=20, verbose_name=_("Contact"), blank=True)
    email = models.EmailField(verbose_name=_("Email"), blank=True)
    address = models.TextField(blank=True, verbose_name=_("Adresse"))
    #  town = models.ForeignKey(
    #      Town, verbose_name=_('Town'), on_delete=models.DO_NOTHING)
    city = models.ForeignKey(
        City, verbose_name=_("Ville"), on_delete=models.DO_NOTHING)

    def save(self, *args, **kwargs):
        if not self.code:
            self.code = get_zfill_data(get_branch_count(), 3)
        return super(Branch, self).save(*args, **kwargs)

    class Meta:
        verbose_name_plural = _("Branches")


# Manage profile here because of Import Error ---------------------------------
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.DO_NOTHING)
    uid = models.UUIDField(default=uuid.uuid4, editable=False, db_index=True)
    work_phone = models.CharField(
        max_length=15, blank=True, verbose_name=_("Contact 1"))
    home_phone = models.CharField(
        max_length=15, blank=True, verbose_name=_("Contact 2"))
    location = models.TextField(blank=True, verbose_name=_("Addresse"))
    id_proof = models.CharField(
        max_length=150, blank=True, verbose_name=_("Matricule"))
    branch = models.ForeignKey(
        Branch, verbose_name=_("Branch"),
        on_delete=models.DO_NOTHING, blank=True, null=True)
    status = models.BooleanField(default=True, verbose_name=_("Statut"))

    def __str__(self):
        return "%s" % self.user

    class Meta:
        verbose_name = _('Utilisateur')
        ordering = ('user',)


# OAuth User permissions
# Afin de gerer des Permission sur des menus qui ne sont pas des Tables
# (Exemple: Dashboard, Analytiques, Grapiques...) Nous usons des Permissions
# gerees par la Class Meta des Modeles
class UserboardPermission(models.Model):

    def get_group_permissions(self, group):
        data = list()
        if group in [_.name for _ in Group.objects.all()]:
            if group == 'admin':
                data = [
                    ("can_create_user", _("Peut créer et gérer des Utilisateurs")),
                    ("can_create_branch", _("Peut créer et gérer des Services")),
                    ("can_disable_branch", _("Peut désactiver des Services")),
                ]

            elif group == 'user':
                data = []

        return data

    class Meta:
        permissions = (
            ("view_dashboard", _("Peut visualiser le Tableau de Bord")),
            ("can_create_user", _("Peut créer et gérer des Utilisateurs")),
            ("can_create_branch", _("Peut créer et gérer des Branches")),
        )


# Branch Counter
class ParamCountBranches(models.Model):
    count = models.IntegerField(default=0)


# ---- Actions ----------------------------------------------------------------
def get_zfill_data(data, width):
    return "{data}".format(data=data).zfill(width)


def get_branch_count():
    obj = ParamCountBranches.objects.filter(id=1)
    if bool(obj):
        return obj[0].count + 1
    return 1


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
