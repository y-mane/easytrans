#!/usr/bin/env python
# -*- coding: utf-8 -*-
from ..models.base import User

from django.contrib import admin
from oauth.models.base import *


@admin.register(City)
class OAUTH_BASE_ADMIN(admin.ModelAdmin):
    search_fields = ['name', 'reference', 'description']
    list_display = ['reference', 'name', 'description']


@admin.register(UserLang)
class USERLANG_ADMIN(admin.ModelAdmin):
    search_fields = ['user__username', 'user__first_name',
                     'user__last_name', 'lang']
    list_display = ['user', 'lang']


@admin.register(UserRecover)
class USERRECOVER_ADMIN(admin.ModelAdmin):
    search_fields = ['user__username', 'user__first_name',
                     'user__last_name', 'recover_code']
    list_display = ['user', 'recover_code']


@admin.register(Town)
class TOWN_ADMIN(admin.ModelAdmin):
    search_fields = ['name', 'reference', 'description', 'city__name']
    list_display = ['reference', 'name', 'city', 'description']


@admin.register(Branch)
class BRANCH_ADMIN(admin.ModelAdmin):
    date_hierarchy = 'created_at'
    search_fields = [
        'name', 'description', 'reference', 'address',
        'city__name']
    list_display = [
        'reference', 'name', 'city', 'phone', 'email', 'address']
    list_filter = ['created_at']


@admin.register(Profile)
class PROFILE_ADMIN(admin.ModelAdmin):
    search_fields = [
        'user__username', 'user__first_name', 'user__last_name',
        'uid', 'id_proof', 'location',
    ]
    list_display = [
        'user', 'id_proof', 'work_phone', 'home_phone', 'location']
    # list_filter = ['role']
    
    
#admin.site.register(User)