#!/usr/bin/env python
# -*- coding: utf-8 -*-


from django import forms
# from core.libs.functions import get_forms_choices
from core.forms.base import BaseForm


# Recuperation formatee de tous les types d'evenements
#  customer_categories = get_forms_choices('CustomerCategory')
#  customer_types = get_forms_choices('CustomerType')
#  quarters = get_forms_choices('Quarter')


# Classe de Gestion des formulaires Evenements pour la Validation avant
# Insertion / Mise a jour
class TicketForm(BaseForm):
    def __init__(self, *args, **kwargs):
        tickettypes = kwargs.pop('tickettypes')
        ticketcategories = kwargs.pop('ticketcategories')
        owners = kwargs.pop('owners')
        super(TicketForm, self).__init__(*args, **kwargs)
        self.fields['ticket_type'] = forms.ChoiceField(
            choices=tickettypes, required=True)
        self.fields['ticket_category'] = forms.ChoiceField(
            choices=ticketcategories, required=True)
        self.fields['owner'] = forms.ChoiceField(
            choices=owners, required=True)


class TicketContentForm(BaseForm):
    def __init__(self, *args, **kwargs):
        tickets = kwargs.pop('tickets')
        super(TicketContentForm, self).__init__(*args, **kwargs)
        self.fields['ticket'] = forms.ChoiceField(
            choices=tickets, required=True)

    reply_from = forms.ChoiceField(
        choices=[('support', 'Support'), ('user', 'User')], required=True)
    content = forms.CharField(required=False)


class TicketCategoryForm(BaseForm):

    def __repr__(self):
        pass


class TicketTypeForm(BaseForm):

    def __repr__(self):
        pass
