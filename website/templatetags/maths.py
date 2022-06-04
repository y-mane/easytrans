#!/usr/bin/env python
# -*- coding: utf-8 -*-


from django import template
import datetime


register = template.Library()


@register.filter
def div(value, arg):
    try:
        return int(int(value)/int(arg))
    except Exception:
        return 0


@register.filter
def percentage(value, arg):
    try:
        return int(int(value)/int(arg) * 100)
    except Exception:
        return 0


@register.filter
def intime(value):
    try:
        # get delay between value to today, format and remove hours and mn
        return (datetime.date.today() - value).total_seconds() <= 0

    except Exception:
        return 0


@register.filter
def reduce(value, width):
    return value[:width]
