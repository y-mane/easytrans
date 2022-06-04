#!/usr/bin/env python
# -*- coding: utf-8 -*-


#  from django.conf.urls import url
from django.urls import path
from django.conf.urls import include
from django.conf import settings
from django.conf.urls.static import static
from website.views import userspace as base
from website.views.userspace import change_state,change_voyage_state,annulation_mission
from oauth.urls import base as auth_urls

urlpatterns = [
    path('', include(auth_urls)),

    # -------------------------------------------------------------------------
    # Dashboard
    # -------------------------------------------------------------------------
    path('dashboard', base.index, name='userspace_index'),
    path('dashboard', base.index, name='landing_index'),
    path('traitement/',base.traitement,name="traitement"),
    path('traitement/<str:pk>',base.traitement,name="traitement"),
    path('livré/<str:pk>',base.livraison,name='livraison'),
    path('annulation/<str:pk>',annulation_mission,name='annulation_mission'),
    path('ajax/change_state/',change_state,name='ajax_change_state'), #change state
    path('change_voyage_state/<str:pk>',change_voyage_state,name="change_voyage_state"),
    path('tickets', base.tickets, name='userspace_tickets'),
    path('notifications', base.notifications,
        name='userspace_notifications'),

    # -------------------------------------------------------------------------
    # Admin
    # -------------------------------------------------------------------------
    path('manage-users', base.manage_users, name='userspace_manage_users'),
    path('manage-branches/', base.manage_branches,
        name='userspace_manage_branches'),
    path('manage-branches/<int:branch>/', base.manage_branch_detail,
        name='userspace_branch_details'),
    path('manage-branches/<int:branch>/enable/', base.manage_enable_branch,
        name='userspace_enable_branch'),
    path('manage-branches/<int:branch>/disable/',
        base.manage_disable_branch, name='userspace_disable_branch'),
    path('manage-users/<int:user>/enable/', base.enable_user,
        name='userspace_enable_user'),
    path('manage-users/<int:user>/disable/', base.disable_user,
        name='userspace_disable_user'),
    path('manage-users-permissions/', base.manage_users_permissions,
        name='userspace_manage_user_permissions'),
    path('manage-users-perms/<int:user>/manage/',
        base.get_users_permissions,
        name='userspace_manage_user_get_permissions'),
    path('manage-users/<int:user>/manage/', base.manage_user_details,
        name='userspace_manage_user_details'),

]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(
        settings.STATIC_URL, document_root=settings.STATIC_ROOT)
