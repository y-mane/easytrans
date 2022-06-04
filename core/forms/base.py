#!/usr/bin/env python
# -*- coding: utf-8 -*-


from django import forms
# from core.libs.functions import get_forms_choices


# Classe de Gestion des formulaires Evenements pour la Validation avant
# Insertion / Mise a jour
class BaseForm(forms.Form):
    name = forms.CharField(max_length=250, required=False)
    # Because we'll generate reference automatically we set ip False in form
    reference = forms.CharField(max_length=250, required=False)
    code = forms.CharField(max_length=10, required=False)
    description = forms.CharField(required=False)
