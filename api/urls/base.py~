#!/usr/bin/env python
# -*- coding: utf-8 -*-


from django.urls import path
from django.conf.urls import include
from rest_framework.routers import DefaultRouter
from api.views.activity import *


router = DefaultRouter()


# router.register(r'tickets', TicketViewSet)


urlpatterns = [
    path('', include(router.urls)),
    path('groups-perms/', group_perms, name="get_groups_permissions"),
    path('groups-perms/<str:g>-group/', group_perms, name="get_groups_permissions"),
]
