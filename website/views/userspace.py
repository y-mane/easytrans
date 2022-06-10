#!/usr/bin/env python
# -*- coding: utf-8 -*-


import logging
# import yaml
import json
from multiprocessing import context
from os import name
# import os
#  import datetime
#  import requests
from django.shortcuts import render,redirect
from django.urls import reverse_lazy, reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import permission_required
# from django.utils.translation import ugettext_lazy as _
# from django.utils import translation
from django.http import HttpResponseRedirect, HttpResponse
from django.http import HttpResponseForbidden
from django.conf import settings
#  from django.views.decorators.csrf import csrf_exempt

from sentry.libs.functions import accesslog

from core.libs.functions import get_forms_choices
from core.libs.functions import get_notification_content
from core.libs.functions import get_model_data
from core.libs.functions import get_user_profile
from oauth.libs.functions import disable_branch
from oauth.libs.functions import enable_branch
from oauth.libs.functions import disable_app_user
from oauth.libs.functions import enable_app_user
from oauth.libs.functions import get_app_user_detail
from oauth.libs.functions import get_branch_details
from oauth.libs.functions import get_user_id        
from oauth.libs.functions import get_user_branch
from oauth.libs.functions import get_app_users
from oauth.libs.functions import check_user_group
from oauth.libs.functions import check_mission_state
from oauth.libs.functions import get_user_front_permissions
from oauth.libs.functions import get_user_groups
from oauth.libs.functions import show_user_permissions

from website.libs.functions import handle_view_get
from website.libs.functions import handle_view_post
from website.libs.functions import get_template
from website.libs.functions import handle_user_manage
from website.libs.functions import handle_user_perms_manage
from start_form.models import Voyage,Mission
from start_form.forms import MissionForm, VoyageForm

from django.contrib.auth.models import User
import mimetypes

paymentlog = logging.getLogger('payment')
debug = logging.getLogger('debug')

@login_required(login_url=reverse_lazy('auth_login'), redirect_field_name=None)
@accesslog
@permission_required('oauth.view_dashboard', raise_exception=True)
def index(request):   
    voyage=Voyage.objects.filter(etat_paiement='succes').order_by('-id')[:]
    voyage_total=voyage.count()
    voyage_en_cours=Voyage.objects.filter(statut_commande='en attente').count()
    voyage_valide=Voyage.objects.filter(statut_commande='validée').count()
    voyage_echouee=Voyage.objects.filter(statut_commande='échouée').count()
    mission=Mission.objects.filter(livreur=request.user).order_by('-voyage')
    myusers=User.objects.all()
    livreurs=check_user_group(myusers)
    mission_total=mission.count()
    mission_acheve=len(check_mission_state(mission,'achevé'))
    mission_en_cours=len(check_mission_state(mission,'en cours'))
    context = dict()
    page_to_render = settings.FORBIDDEN_ACCESS
    groups = get_user_groups(request.user)
    print("groups: %s" % groups)
    
    voyage_id=request.POST.get('voyage_id')
    if request.method=='POST' :
        livreurform=request.POST.get('livreur')
        livreur_assigner=User.objects.get(id=livreurform)
        voyageform=request.POST.get('voyage')
        voyage_assigner=Voyage.objects.get(id=voyageform)
        commentaire=request.POST.get('commentaire')
        form=Mission.objects.create(livreur=livreur_assigner,voyage=voyage_assigner,commentaire=commentaire)
        form.save()
        
    if bool(groups):
        page_to_render = get_template("%s_dashboard.html" % groups[0], 2)
        context['user'] = request.user
        context['profile'] = get_user_profile(request.user)
        context['user_front_perm'] = get_user_front_permissions(request.user)
        context['voyage']=voyage
        #context['form']=form
        context['mission']=mission
        context['voyage_total']=voyage_total
        context['mission_total']=mission_total
        context['livreurs']=livreurs
        context['voyage_en_cours']=voyage_en_cours 
        context['voyage_valide']=voyage_valide
        context['voyage_echouee']=voyage_echouee  
        context['mission_acheve']=mission_acheve 
        context['mission_en_cours']=mission_en_cours 
    return render(request, page_to_render, context)

def change_voyage_state(request,pk):
    if request.method=='GET':
        voyage=Voyage.objects.get(id=pk)
        voyage.statut_commande=Voyage.STATUT[0][0]
        voyage.save()
        return redirect('userspace_index')
        #return HttpResponse("Success!") # Sending an success response
    else:
         return HttpResponse("Request method is not a GET")


def change_state(request):
    if request.method=='GET':
        voyage_id=request.GET['event_id']
        voyage=Voyage.objects.get(id=voyage_id)
        voyage.statut_commande='validée'
        return HttpResponse("Success!") # Sending an success response
    else:
         return HttpResponse("Request method is not a POST")
    #return JsonResponse(list(gars.values('id', 'name')), safe=False)
    #return render(request,'website/back/trnt.html',context)


def traitement(request,pk):
    voyage=Voyage.objects.get(id=pk)
    if request.method == "GET":
        voyage.statut_commande=Voyage.STATUT[1][0]
        voyage.save()
        return redirect('userspace_index')
    context={}
    #return render (request,'website/back/traitement.html',context)

def livraison(request,pk):
    mission=Mission.objects.get(id=pk)
    if request.method=='GET':
        mission.voyage.etat_voyage=Voyage.ETAT[1][0]
        mission.voyage.save()
        return redirect('userspace_index')
    context={}
    return render(request,'website/back/livraison.html',context)

def annulation_mission(request,pk):
    mission=Mission.objects.get(id=pk)
    if request.method=='GET':
        mission.voyage.etat_voyage=Voyage.ETAT[0][0]
        mission.voyage.save()
        return redirect('userspace_index')
    

"""def mission(request):
    context={}
    #groups = get_user_groups(request.user)
    #print("groups: %s" % groups)
    #user=get_user_id(request.user)
    mission=Mission.objects.filter(livreur=request.user)
    #if groups=='livreur':
    context['mission']=mission
         
    return render(request,'website/back/mission.html',context)"""








@login_required(login_url=reverse_lazy('auth_login'), redirect_field_name=None)
@accesslog
@permission_required('oauth.view_dashboard', raise_exception=True)
def notifications(request):
    ''' Manage Web Notifications. will be sent after each actions '''
    context = dict()
    context['branch'] = get_user_branch(request.user.id)
    context['user_id'] = request.user.id
    context['infos'] = get_notification_content(
        request.user.id, request.session.get('infos', 0))
    context['infos_type'] = request.session.get('infos_type', 0)
    request.session.pop('infos', None)
    request.session.pop('infos_type', None)
    return render(request, "website/back/notifications.html", context)


@login_required(login_url=reverse_lazy('auth_login'), redirect_field_name=None)
@accesslog
@permission_required('oauth.view_dashboard', raise_exception=True)
def tickets(request):
    ''' Manage Tickets. @deprecated '''
    if request.method == 'GET':
        page_to_render = settings.FORBIDDEN_ACCESS
        data_for_page = {
            'fields': [
                ('ticketcategories', 'TicketCategory'),
                ('tickettypes', 'TicketType')
            ],
            'params': {'status': True},
            'filter': {'order_by': 'id', 'limit': 50}
        }
        data_for_user = {
            'fields': [('tickets', 'Ticket')],
            'params': {'status': True},
            'filter': {'order_by': 'id', 'limit': 50}
        }
        groups = get_user_groups(request.user)
        #  page_to_render = display_page.get(groups[0], None) or '403.html'
        if bool(groups):
            page_to_render = get_template("%s_tickets.html" % groups[0], 2)
        return handle_view_get(
            request, data_for_page, data_for_user, page_to_render)

    elif request.method == 'POST':
        return handle_view_post(
            request, 'TicketForm',
            {'owners': get_forms_choices('User'),
             'tickettypes': get_forms_choices('TicketType'),
             'ticketcategories': get_forms_choices('TicketCategory')},
            'handle_ticket', ['name', 'description', 'ticket_type',
                              'ticket_category', 'owner'], 'ticket_id',
            'userspace_tickets', 'userspace_tickets')

    else:
        return HttpResponseForbidden(json.dumps(['Forbidden Access']))


@login_required(login_url=reverse_lazy('auth_login'), redirect_field_name=None)
@accesslog
@permission_required('oauth.view_dashboard', raise_exception=True)
def manage_users_permissions(request):
    if request.method == 'POST':
        return handle_user_perms_manage(request)

    else:
        return HttpResponseForbidden(json.dumps(['Forbidden Access']))


@login_required(login_url=reverse_lazy('auth_login'), redirect_field_name=None)
@accesslog
@permission_required('oauth.view_dashboard', raise_exception=True)
def get_users_permissions(request, user):
    if request.method == 'GET':
        data = show_user_permissions(user)
        return HttpResponse(data)

    else:
        return HttpResponseForbidden(json.dumps(['Forbidden Access']))


@login_required(login_url=reverse_lazy('auth_login'), redirect_field_name=None)
@accesslog
@permission_required('oauth.view_dashboard', raise_exception=True)
def manage_users(request):
    if request.method == 'GET':
        context = dict()
        page_to_render = settings.FORBIDDEN_ACCESS
        groups = get_user_groups(request.user)
        if bool(groups):
            page_to_render = get_template("%s_users.html" % groups[0], 2)
        context['users'] = get_app_users()
        context['profile'] = get_user_profile(request.user)
        context['groups'] = get_model_data('Group')
        context['branches'] = get_model_data(
            'Branch', filter_params={'status': True}, limit=150)
        context['user_id'] = request.user.id
        context['infos'] = get_notification_content(
            request.user.id, request.session.get('infos', 0))
        context['infos_type'] = request.session.get('infos_type', 0)
        request.session.pop('infos', None)
        request.session.pop('infos_type', None)
        return render(request, page_to_render, context)

    elif request.method == 'POST':
        return handle_user_manage(request)

    else:
        return HttpResponseForbidden(json.dumps(['Forbidden Access']))


@login_required(login_url=reverse_lazy('auth_login'), redirect_field_name=None)
@accesslog
@permission_required('oauth.view_dashboard', raise_exception=True)
def manage_user_details(request, user):
    if request.method == 'GET':
        context = get_app_user_detail(user)
        return HttpResponse(json.dumps(context))
    else:
        return HttpResponseForbidden(json.dumps(['Forbidden Access']))


@login_required(login_url=reverse_lazy('auth_login'), redirect_field_name=None)
@accesslog
@permission_required('oauth.view_dashboard', raise_exception=True)
def disable_user(request, user):
    if request.method == 'GET':
        try:
            disable_app_user(user)
            request.session['infos'] = 700
            request.session['infos_type'] = 1
            debug.debug("[+] Enabled User: {}".format(user))
        except Exception as e:
            request.session['infos'] = 702
            request.session['infos_type'] = 2
            debug.debug("[x] Got Exception: {ex} while disabling User:"
                        " {b}".format(ex=str(e), b=user))
        return HttpResponseRedirect(reverse('userspace_manage_users'))
    else:
        return HttpResponseForbidden(json.dumps(['Forbidden Access']))


@login_required(login_url=reverse_lazy('auth_login'), redirect_field_name=None)
@accesslog
@permission_required('oauth.view_dashboard', raise_exception=True)
def enable_user(request, user):
    if request.method == 'GET':
        try:
            enable_app_user(user)
            request.session['infos'] = 700
            request.session['infos_type'] = 1
            debug.debug("[+] Enabled User: {}".format(user))
        except Exception as e:
            request.session['infos'] = 702
            request.session['infos_type'] = 2
            debug.debug("[x] Got Exception: {ex} while enabling User:"
                        " {b}".format(ex=str(e), b=user))
        return HttpResponseRedirect(reverse('userspace_manage_users'))
    else:
        return HttpResponseForbidden(json.dumps(['Forbidden Access']))


@login_required(login_url=reverse_lazy('auth_login'), redirect_field_name=None)
@accesslog
@permission_required('oauth.view_dashboard', raise_exception=True)
def manage_branches(request):
    if request.method == 'GET':
        context = dict()
        page_to_render = settings.FORBIDDEN_ACCESS
        groups = get_user_groups(request.user)
        if bool(groups):
            page_to_render = get_template("%s_branches.html" % groups[0], 2)
        context['profile'] = get_user_profile(request.user)
        context['branches'] = get_model_data('Branch', limit=150)
        context['cities'] = get_model_data('City', limit=150)
        context['user_id'] = request.user.id
        context['infos'] = get_notification_content(
            request.user.id, request.session.get('infos', 0))
        context['infos_type'] = request.session.get('infos_type', 0)
        request.session.pop('infos', None)
        request.session.pop('infos_type', None)
        return render(request, page_to_render, context)

    elif request.method == 'POST':
        return handle_view_post(
            request, 'BranchForm',
            {'cities': get_forms_choices('City')}, 'set_branch',
            ['name', 'phone', 'email', 'address', 'city'],
            'branch_id', 'userspace_manage_branches',
            'userspace_manage_branches')

    else:
        return HttpResponseForbidden(json.dumps(['Forbidden Access']))


@login_required(login_url=reverse_lazy('auth_login'), redirect_field_name=None)
@accesslog
@permission_required('oauth.view_dashboard', raise_exception=True)
def manage_branch_detail(request, branch):
    if request.method == 'GET':
        context = get_branch_details(branch)
        return HttpResponse(json.dumps(context))

    else:
        return HttpResponseForbidden(json.dumps(['Forbidden Access']))


@login_required(login_url=reverse_lazy('auth_login'), redirect_field_name=None)
@accesslog
@permission_required('oauth.view_dashboard', raise_exception=True)
def manage_enable_branch(request, branch):
    if request.method == 'GET':
        try:
            enable_branch(branch)
            request.session['infos'] = 700
            request.session['infos_type'] = 1
            debug.debug("[+] Enabled Branch: {}".format(branch))
        except Exception as e:
            request.session['infos'] = 702
            request.session['infos_type'] = 2
            debug.debug("[x] Got Exception: {ex} while enabling Branch:"
                        " {b}".format(ex=str(e), b=branch))
        return HttpResponseRedirect(reverse('userspace_manage_branches'))
    else:
        return HttpResponseForbidden(json.dumps(['Forbidden Access']))


@login_required(login_url=reverse_lazy('auth_login'), redirect_field_name=None)
@accesslog
@permission_required('oauth.view_dashboard', raise_exception=True)
def manage_disable_branch(request, branch):
    if request.method == 'GET':
        try:
            disable_branch(branch)
            request.session['infos'] = 700
            request.session['infos_type'] = 1
            debug.debug("[+] Disabled Branch: {}".format(branch))
        except Exception as e:
            request.session['infos'] = 702
            request.session['infos_type'] = 2
            debug.debug("[x] Got Exception: {ex} while disabling Branch:"
                        " {b}".format(ex=str(e), b=branch))
        return HttpResponseRedirect(reverse('userspace_manage_branches'))
    else:
        return HttpResponseForbidden(json.dumps(['Forbidden Access']))
