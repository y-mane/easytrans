#!/usr/bin/env python
# -*- coding: utf-8 -*-


from django.contrib import admin


#  @admin.register(NotificationType, TicketCategory, TicketType)
#  class BASE_ADMIN(admin.ModelAdmin):
#      date_hierarchy = 'created_at'
#      search_fields = ['name', 'description', 'reference']
#      list_display = ['name', 'reference', 'status', 'created_at']
#      list_filter = ['created_at']
#
#
#  @admin.register(Ticket)
#  class TICKET_ADMIN(admin.ModelAdmin):
#      date_hierarchy = 'created_at'
#      search_fields = [
#          'name', 'description', 'reference', 'ticket_category__name',
#          'ticket_type__name', 'owner__username', 'owner__first_name',
#          'owner__last_name',
#      ]
#      list_display = ['name', 'reference', 'ticket_type', 'ticket_category',
#                      'owner', 'status', 'created_at']
#      list_filter = ['created_at']
