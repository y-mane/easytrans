#!/usr/bin/env python
# -*- coding: utf-8 -*-


from django.core.paginator import Paginator
#  from django.core.paginator import PageNotAnInteger
from django.db import IntegrityError
from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponseRedirect
#  from django.utils.crypto import get_random_string
from django.core.files.storage import FileSystemStorage
#  from django.utils.translation import ugettext_lazy as i18_
from django.conf import settings
from oauth.models.base import UserLang
from core.libs.functions import *
from oauth.libs.functions import *
from oauth.forms.base import *
from core.libs.errors import *
from core.forms.tickets import *
from core.forms.notifications import *
from datetime import datetime
import time
import os
import json
import logging
import requests
from django.utils import translation


WEB_TEMPLATES_FOLDER = os.path.join(
    os.path.dirname(settings.BASE_DIR), 'website/templates')
BASE_FRONT_TEMPLATES = 'website/front'
BASE_BACK_TEMPLATES = 'website/back'


log = logging.getLogger('debug')


def handle_form(form, fields, action=1):
    """
        Function to encapsulate form handling for avoiding
        cleaning form in views
    """
    data = dict()
    if action == 1:
        for _ in fields:
            data[_] = form.cleaned_data[_]
        log.debug("[!] [handle_form] got form: {form} for handling {fields}. \
                  Returning: {data}".format(data=data, form=form,
                  fields=fields))
        return data
    else:
        # wanted to record data in this section but....
        pass


def handle_view_post(request, form, form_kwargs, callback, fields_to_manage,
                     id_field, success_page, error_page):
    '''
        @param request: Request passed to view
        @param form: django form used to manage POST request. string name
            provided because we'll evaluate name before using.
        @param form_kwargs: dict passed to form for handling it
        @param callback: function used to handle cleaned form (Posted form)
        @param fields_to_manage: list of fields to cleaning data
            (method of forms)
        @param id_field: name of field used to check if it's an update
        @param succes_page: string of page used to redirect. have to be
            reversed string
        @param error_page: reversed page to render in case of error
    '''
    # Bulk renaming files before handling them
    handle_request_file(request.FILES)
    # log purpose
    log.info("[!] got quietly POST request: {}".format(request.POST))
    log.debug("[!] [handle_view_post] got form: {form} with {kwargs} "
              "for handling {fields} with callback: {callback}. [?] record ID "
              "present ? (ID: {record_id})."
              " Incase of success returning: {success}"
              " otherwise error thown and page {error} returned.".format(
                  form=form, kwargs=form_kwargs, callback=callback,
                  record_id=request.POST.get(id_field, None),
                  success=success_page, error=error_page,
                  fields=fields_to_manage))

    # Updating dict request.FILES to be handled by for as **kwargs
    action = 1
    model_id = None

    model_form = eval(form)(request.POST, request.FILES, **form_kwargs)
    log.debug("[?] Is form valid ?: %s" % model_form.is_valid())
    if model_form.is_valid():
        # Moving files before processing entirely form
        for rFilename, rFile in request.FILES.items():
            handle_uploaded_file(rFile)
        # Logging
        log.info("[+] Got valid model_form: {}".format(
            model_form.cleaned_data))
        data = handle_form(model_form, fields_to_manage)
        log.info("[+] Got cleaned data for record: {}".format(data))
        if bool(request.POST.get(id_field, None)):
            action = 2
            model_id = request.POST.get(id_field, None)

        eval(callback)(data, action, model_id)
        request.session['infos'] = 700
        request.session['infos_type'] = 1
        return HttpResponseRedirect(reverse(success_page))

    else:
        log.info("[x] Got infos in form data: {}".format(
            model_form.errors.as_json(escape_html=True)))
        # infos = json.loads(model_form.errors.as_json(escape_html=True))
        request.session['infos'] = 701
        request.session['infos_type'] = 2
        return HttpResponseRedirect(reverse(error_page))


def handle_view_get(request, single_fields, fields_for_owner, redirect_page):
    """
    @param request: Http request passed through query
    @param single_fields: dict containing list of tuples which are name of
        foreign keys variables used for looping and associated Models.
        Ex: [('users', 'User')]. key params containing filter params used to
        retrieve results.
    @param fields_for_owner: same as single_field however result are related to
        specific owner. result depends on model field owner
        (logged_user by default)
    @param redirect_page: html page which will be rendered.
    """
    log.debug("[!] [handle_view_get] handling {fields} and {other_fields} for "
              "an owner [{owner}:{id}]. Redirecting page to: {redirect}".format(
                  fields=single_fields, other_fields=fields_for_owner,
                  owner=request.user.username, id=request.user.id,
                  redirect=redirect_page))
    log.debug(
        "[?] Is django language same as user language: %s" % check_lang(
            request))
    context = dict()
    # specific for this project - not expand to all
    context['branch'] = get_user_branch(request.user.id)
    context['user_profile'] = get_user_profile(request.user.id)
    # By default we put user.id in dict we pass to view to retrieve it later
    context['user'] = request.user
    context['infos'] = get_notification_content(
        request.user.id, request.session.get('infos', 0))
    context['infos_type'] = request.session.get('infos_type', 0)
    if bool(single_fields):
        for _ in single_fields['fields']:
            # add [::-1] for reversing list. otherwise do it in template
            context[_[0]] = get_model_data(
                _[1], single_fields['params'],
                single_fields['filter']['order_by'],
                single_fields['filter']['limit'])

    if bool(fields_for_owner):
        for _ in fields_for_owner['fields']:
            context[_[0]] = get_model_data_for_owner(
                _[1], fields_for_owner['params'],
                fields_for_owner['filter']['order_by'],
                fields_for_owner['filter']['limit'],
                request.user.id)
    # Deleting infos dict passed from post view to get view through session
    log.info("[+] got infos: {}".format(request.session.get('infos', None)))
    request.session.pop('infos', None)
    request.session.pop('infos_type', None)
    log.info("[+] got context before passing to view: {}".format(context))
    # Raising error just for testing purpose. mail_admins
    #  raise ValueError("I want django to send error 500")
    return render(request, redirect_page, context)


def handle_view_get_for_paginator(request, single_fields, redirect_page,
                                  model, model_filters=dict()):
    """
    @param request: Http request passed through query
    @param model: model which will be used for paginating
    @param model_filters: dict of filters we want to apply to model
    @param single_fields: dict containing list of tuples which are name of
        foreign keys variables used for looping and associated Models.
        Ex: [('users', 'User')]. key params containing filter params used to
        retrieve results.
    @param redirect_page: html page which will be rendered.
    """

    log.debug("[!] [handle_view_get] handling {fields} for" +
              "an owner [{owner}:{id}]. Redirecting page to: {redirect}".format(
                  fields=single_fields, owner=request.user.username,
                  redirect=redirect_page, id=request.user.id))

    context = dict()
    context['user'] = request.user
    context['infos'] = get_notification_content(
        request.user.id, request.session.get('infos', 0))
    context['infos_type'] = request.session.get('infos_type', 0)
    if bool(single_fields):
        for _ in single_fields['fields']:
            # add [::-1] for reversing list. otherwise do it in template
            context[_[0]] = get_model_data(
                _[1], single_fields['params'],
                single_fields['filter']['order_by'],
                single_fields['filter']['limit'])

    # Paginating Function. first we get current page otherwise first page
    # returned
    page = request.GET.get('page', 1)
    datas = get_model_paginator(model, model_filters)
    paginator = Paginator(datas, 1)
    context['data'] = paginator.get_page(page)
    context['data_count'] = paginator.count
    context['number_of_pages'] = paginator.num_pages
    context['page_range'] = paginator.page_range
    context['current_page'] = page

    log.info("[!] got context before passing to view: {}".format(context))
    log.info("[+] got infos: {}".format(request.session.get('infos', 0)))
    request.session.pop('infos', None)
    request.session.pop('infos_type', None)
    log.info("[+] got context before passing to view: {}".format(context))
    return render(request, redirect_page, context)


def handle_user_manage(request):
    data = {k: v for k, v in request.POST.items()}
    data.pop('csrfmiddlewaretoken', None)
    log.debug("[+] Handle user create got data {}".format(data))
    log.debug("[?] check status of user_id: {}".format(bool(data['user_id'])))
    log.debug("data: {}".format(data))
    try:
        if bool(data['user_id']):
            update_app_user(data)
        else:
            data.pop('user_id', None)
            set_app_user(data)
        request.session['infos'] = 700
        request.session['infos_type'] = 1
        # log.debug("[+] Handled user create got record {}".format(record))
    except IntegrityError as ie:
        request.session['infos'] = 706
        request.session['infos_type'] = 2
        log.debug("[x] Got Exception: {}".format(str(ie)))
    except Exception as e:
        request.session['infos'] = 702
        request.session['infos_type'] = 2
        log.debug("[x] Got Exception: {}".format(str(e)))
    return HttpResponseRedirect(reverse('userspace_manage_users'))


def handle_user_perms_manage(request):
    data = {k: v for k, v in request.POST.items()}
    data.pop('csrfmiddlewaretoken', None)
    log.debug("[+] got data from post {}".format(data))
    data['permissions'] = data['permissions'].split(',')

    try:
        if bool(data['puser_id']):
            set_app_user_perms(data)

        request.session['infos'] = 700
        request.session['infos_type'] = 1

    except Exception as e:
        request.session['infos'] = 702
        request.session['infos_type'] = 2
        log.debug("[x] Got Exception: {}".format(str(e)))
    return HttpResponseRedirect(reverse('userspace_manage_users'))


def check_captcha(captcha):
    url = settings.GOOGLE_URL_CAPTCHA_CHECK
    data = {
        'secret': settings.GOOGLE_RECAPTCHA_SECRET_KEY,
        'response': captcha
    }
    check_process = requests.post(url, data=data)
    log.debug("[+] got check_process text: %s" % check_process.text)
    result = json.loads(check_process.text)
    log.debug("[+] got result to send back: {}".format(result))
    return result


def format_str_to_date(str_date):
    obj = datetime.strptime(str_date, '%m/%d/%Y')
    # return str(obj.date())
    return obj.date()


def handle_uploaded_files(f):
    with open('destination', 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)


def rename(filename):
    extension = filename.split(".")[-1]
    return "%s.%s" % (time.strftime('%d%m%Y_%H%M%S'), extension)


def handle_request_file(rFiles):
    cpt = 0
    for rFilename, rFile in rFiles.items():
        log.info("Filename from form: %s" % rFilename)
        extension = rFile.name.split(".")[-1]
        rFile.name = "%s_%s.%s" % (
            time.strftime('%d%m%Y_%H%M%S'), cpt, extension)
        cpt += 1
        log.info("File : %s" % rFile)


def handle_uploaded_file(rFile, rDestination=settings.MEDIA_ROOT):
    fs = FileSystemStorage()
    fs.save(os.path.join(rDestination, rFile.name), rFile)


def get_template(template_name, template_type):
    '''
       Get templates or 403.html. could use get_template from django template
       loader
    '''
    template = "%s/%s" % (BASE_FRONT_TEMPLATES, template_name) if \
        template_type == 1 else "%s/%s" % (BASE_BACK_TEMPLATES, template_name)
    if os.path.exists(os.path.join(WEB_TEMPLATES_FOLDER, template)):
        return template
    return settings.FORBIDDEN_ACCESS


def get_app_template(app_tpl_dir, tpl_name):
    app_tpl_folder = os.path.join(
        os.path.dirname(settings.BASE_DIR), '%s/templates' % app_tpl_dir)
    if os.path.exists(os.path.join(app_tpl_folder, tpl_name)):
        return tpl_name
    return settings.FORBIDDEN_ACCESS


def check_lang(request):
    dlang = translation.get_language_from_request(request)
    # log.debug("[+] Got dlang: {}".format(dlang))
    lang = 'fr'
    #  user = User.objects.get(id=request.user.id)
    try:
        user_lang = UserLang.objects.get(user=request.user)
        lang = user_lang.lang
    except Exception as e:
        pass
        log.debug("[x] Couldn't get user lang: {}".format(str(e)))
        log.debug("[x] Setting user lang: {}".format(lang))
    #  log.debug("[+] Got user lang: {}".format(lang))
    return dlang == lang


# ------------------------------------------------------------------------------
# Custom
# ------------------------------------------------------------------------------
