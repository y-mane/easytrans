#!/usr/bin/env python
# -*- coding: utf-8 -*-


from django.contrib import admin
from sentry.models.base import *


@admin.register(Action)
class BASE_ADMIN(admin.ModelAdmin):
    date_hierarchy = 'created_at'
    search_fields = [
        'name', 'description', 'reference', 'action_type', 'target',
        'current_value', 'new_value', 'record_class', 'owner__first_name',
        'owner__last_name', 'owner__username']
    list_display = [
        'reference', 'name', 'created_at', 'record_class', 'action_type',
        'target', 'current_value', 'new_value', 'owner']
    list_filter = ['created_at']


@admin.register(CronJob)
class CJ_ADMIN(admin.ModelAdmin):
    date_hierarchy = 'start'
    search_fields = ['reference', 'cron_type']
    list_display = ['reference', 'cron_type', 'start', 'end']
    list_filter = ['cron_type']


@admin.register(CronJobMessage)
class CJMESSAGE_ADMIN(admin.ModelAdmin):
    date_hierarchy = 'created_at'
    search_fields = ['reference', 'message', 'message_type']
    list_display = [
        'cron_job', 'created_at', 'message_type', 'message']
    list_filter = ['created_at']


@admin.register(EmergencyMessage)
class EMESSAGE_ADMIN(admin.ModelAdmin):
    date_hierarchy = 'created_at'
    search_fields = [
        'reference', 'message', 'raw_data', 'motive', 'title', 'receiver']
    list_display = [
        'created_at', 'receiver', 'title', 'code', 'motive', 'message', 'raw_data']
    list_filter = ['created_at']


@admin.register(AuthorizedIPS)
class AIPS_ADMIN(admin.ModelAdmin):
    date_hierarchy = 'created_at'
    search_fields = ['source', 'description']
    list_display = ['created_at', 'name', 'source', 'status', 'description']
    list_filter = ['created_at']


@admin.register(UnAuthorizedIPS)
class UAIPS_ADMIN(admin.ModelAdmin):
    date_hierarchy = 'created_at'
    search_fields = ['source', 'description']
    list_display = ['created_at', 'name', 'source', 'status', 'description']
    list_filter = ['created_at']
