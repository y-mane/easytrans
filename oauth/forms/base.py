#!/usr/bin/env python
# -*- coding: utf-8 -*-


from django import forms
from django.utils.translation import ugettext as _


class LoginForm(forms.Form):
    username = forms.CharField(max_length=150)
    password = forms.CharField(max_length=150)


class BranchForm(forms.Form):
    def __init__(self, *args, **kwargs):
        cities = kwargs.pop('cities')
        super(BranchForm, self).__init__(*args, **kwargs)
        self.fields['city'] = forms.ChoiceField(
            choices=cities, required=True)

    name = forms.CharField(max_length=250, required=False)
    # Because we'll generate reference automatically we set ip False in form
    reference = forms.CharField(max_length=250, required=False)
    code = forms.CharField(max_length=10, required=False)
    description = forms.CharField(required=False)
    phone = forms.CharField(required=False)
    email = forms.EmailField(required=False)
    address = forms.CharField(required=False)

    def __repr__(self):
        return _("Branch Form")


class CityForm(forms.Form):
    name = forms.CharField(max_length=250, required=False)
    # Because we'll generate reference automatically we set ip False in form
    reference = forms.CharField(max_length=250, required=False)
    code = forms.CharField(max_length=10, required=False)
    description = forms.CharField(required=False)

    def __repr__(self):
        return _("City Form")
