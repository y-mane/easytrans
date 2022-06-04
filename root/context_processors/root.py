#!/usr/bin/env python
# -*- coding: utf-8 -*-


from django.conf import settings
from django.utils.translation import ugettext_lazy as _


def global_settings(request):

    return {
        'APP_TITLE': settings.APP_TITLE,
        'BASE_SERVER': settings.BASE_SERVER,
        'USERS_FRONT_PERMS': [
            {'perm': 'can_create_user',
             'name': _("Peut créer et gérer des Utilisateurs")},
            {'perm': 'can_create_branch',
             'name': _("Peut créer et gérer des Branches")},
        ],
    }
