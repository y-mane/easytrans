#!/usr/bin/env python
# -*- coding: utf-8 -*-


# from django.contrib.auth import authenticate
# from django.contrib.auth import login as request_login
# from django.contrib.auth import logout as request_logout
# from django.contrib.auth.decorators import login_required
# from django.urls import reverse_lazy
# from django.views.decorators.csrf import csrf_exempt

# from django.http import HttpResponse

from django.urls import reverse
from django.http import Http404
from django.shortcuts import render
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect
from django.conf import settings
from django.contrib.auth import authenticate
from django.contrib.auth import login as request_login
from django.contrib.auth import logout as request_logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import permission_required

from oauth.forms.base import LoginForm
from oauth.libs.functions import get_user_groups
from oauth.libs.functions import set_recover_code
from oauth.libs.functions import set_user_password
from oauth.libs.functions import set_user_recover_password
from oauth.libs.functions import get_user_lang
from oauth.libs.functions import set_user_lang
from website.libs.functions import handle_view_get
from website.libs.functions import handle_view_post
from website.libs.functions import get_app_template

from sentry.libs.functions import accesslog
from django.utils import translation
import logging
import yaml
import os
import json
import requests


LANGUAGE = translation.get_language()
CURRENT_LANG_DIR = os.path.join(settings.CONFIG_DIR, LANGUAGE)
MESSAGES_FILE = os.path.join(CURRENT_LANG_DIR, settings.MESSAGES_FILE)


with open(MESSAGES_FILE) as mf:
    messages = yaml.load(mf, Loader=yaml.SafeLoader)

default_log = logging.getLogger("default")
debug_log = logging.getLogger("debug")
log = logging.getLogger("request")


def index(request):
    context = dict()
    return render(request, "oauth/login.html", context)


def main_signin(request):
    context = dict()
    loginform = LoginForm(request.POST or None)
    if loginform.is_valid():
        username = loginform.cleaned_data['username']
        password = loginform.cleaned_data['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            print("user: %s" % user)
            request_login(request, user)
            user_lang = get_user_lang(user)
            debug_log.debug(
                "[+] while login got request user lang:"
                " %s" % translation.get_language_from_request(request))
            debug_log.debug(
                "[+] while login got default user lang: %s" % user_lang)
            translation.activate(user_lang)
            request.session[translation.LANGUAGE_SESSION_KEY] = user_lang
            debug_log.debug(
                "[+] activating user lang: %s" % user_lang)
            return HttpResponseRedirect(reverse('userspace_index'))
        else:
            return render(request, "oauth/login.html", context)
    return render(request, "oauth/login.html", context)
#
#
#  def main_signin(request):
#      payload = dict()
#      payload['username'] = request.POST.get('username', str())
#      payload['password'] = request.POST.get('password', str())
#      url = request.build_absolute_uri(reverse('base_signin'))
#      response = requests.post(url, data=payload)
#      if response.status_code == 200:
#          #  response_data = response.json()
#          response_data = json.loads(response.text)
#          if 'user' and 'token' in response_data.keys():
#              user = authenticate(
#                  username=payload['username'], password=payload['password'])
#              if user is not None:
#                  request_login(request, user)
#                  user_lang = get_user_lang(user)
#                  debug_log.debug(
#                      "[+] while login got request user lang:"
#                      " %s" % translation.get_language_from_request(request))
#                  debug_log.debug(
#                      "[+] while login got default user lang: %s" % user_lang)
#                  translation.activate(user_lang)
#                  request.session[translation.LANGUAGE_SESSION_KEY] = user_lang
#                  debug_log.debug(
#                      "[+] activating user lang: %s" % user_lang)
#                  return HttpResponseRedirect(reverse('userspace_index'))
#          else:
#              return render(request, "oauth/login.html", context)
#      return render(request, "oauth/login.html", context)


def facebook_signin(request):
    context = dict()
    return render(request, "oauth/login.html", context)


def google_signin(request):
    context = dict()
    return render(request, "oauth/login.html", context)


def linkedin_signin(request):
    context = dict()
    return render(request, "oauth/login.html", context)


def logout(request):
    request_logout(request)
    return HttpResponseRedirect(reverse('auth_index'))


def signup(request):
    context = dict()
    return render(request, "oauth/register.html", context)


def signup_process(request):
    context = dict()
    return HttpResponseRedirect(reverse('auth_index'))


def recover_password_first_step(request):
    context = dict()
    if request.method == 'GET':
        debug_log.debug('[+] Start recovering password ...')
        return render(request, "oauth/recover-password-1.html", context)
    if request.method == "POST":
        username = request.POST.get('username', str())
        debug_log.debug('[+] Got username in request: {}'.format(username))
        query = set_recover_code(username)
        debug_log.debug('[+] After processing username, got result:'
                        '{}'.format(query))
        if bool(query):
            # silent inserting username for following process.
            request.session['username'] = username
            return HttpResponseRedirect(reverse('auth_recover_second'))
        else:
            return render(request, "oauth/808.html", context)
    else:
        return Http404


def recover_password_second_step(request):
    if request.method == 'GET':
        context = dict()
        debug_log.debug('[+] In second form for recovering process...')
        if 'username' in request.session.keys():
            context['username'] = request.session.get('username', str())
            request.session.pop('username', None)
        return render(request, "oauth/recover-password-2.html", context)
    if request.method == 'POST':
        debug_log.debug('[+] In second form for recovering process...'
                        'got request:  {}'.format(
                            {k: v for k,v in request.POST.items()}))
        username = request.POST.get('username', str())
        # in case of direct accessing to url without silent get of username
        if not bool(username):
            return render(
                request, settings.FORBIDDEN_ACCESS, locals())
        # following process
        recover_code = request.POST.get('recover_code', str())
        password = request.POST.get('password', str())
        query = set_user_recover_password(username, password, recover_code)
        debug_log.debug('[+] After processing username, got result:'
                        '{}'.format(query))
        if bool(query):
            return HttpResponseRedirect(reverse('auth_login'))
        return render(request, 'oauth/909.html')


@login_required(login_url=reverse_lazy('auth_login'), redirect_field_name=None)
@accesslog
@permission_required('oauth.view_dashboard', raise_exception=True)
def profile(request):
    data_for_page = dict()
    data_for_user = dict()
    groups = get_user_groups(request.user)
    page_to_render = get_app_template(
        "oauth", "oauth/%s_profile.html" % groups[0])
    return handle_view_get(request, data_for_page, data_for_user, page_to_render)


def profile_edit_process(request):
    context = dict()
    return render(request, "oauth/profile.html", context)


def password_edit_process(request):
    if request.method == 'POST':
        password = request.POST.get('new_password', '')
        try:
            set_user_password(request.user.id, password)
            request.session['infos'] = 700
            request.session['infos_type'] = 1
        except Exception as e:
            request.session['infos'] = 702
            request.session['infos_type'] = 2
            debug_log.debug("[x] Got Exception: {}".format(str(e)))

    return HttpResponseRedirect(reverse('auth_profile'))


def setting_language(request):
    if request.method == "POST":
        language = request.POST.get('language', 'en')
        debug_log.debug(
            "[+] from change app language form, got: %s" % language)
        user_lang = set_user_lang(request.user, language)
        debug_log.debug("[+] after change function, got: %s" % user_lang)
        request.session[translation.LANGUAGE_SESSION_KEY] = user_lang
        return HttpResponseRedirect(reverse('auth_profile'))
    else:
        return Http404
