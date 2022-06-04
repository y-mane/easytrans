#!/usr/bin/env python
# -*- coding: utf-8 -*-


from django import forms
# from core.libs.functions import get_forms_choices
from core.forms.base import BaseForm


class NotificationForm(BaseForm):
    def __init__(self, *args, **kwargs):
        notificationtypes = kwargs.pop('notificationtypes')
        from_users = to_users = kwargs.pop('users')
        super(NotificationForm, self).__init__(*args, **kwargs)
        self.fields['notification_type'] = forms.ChoiceField(
            choices=notificationtypes, required=True)
        self.fields['from_user'] = forms.ChoiceField(
            choices=from_users, required=True)
        self.fields['to_user'] = forms.ChoiceField(
            choices=to_users, required=True)

    content = forms.CharField(required=False)
    priority = forms.IntegerField(required=False)


class NotificationTypeForm(BaseForm):

    def __repr__(self):
        pass
