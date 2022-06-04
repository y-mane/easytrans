#!/usr/bin/python2.7
# -*- coding: UTF-8 -*-


from django.contrib.auth.hashers import make_password
#  from django.db import IntegrityError
from django.utils.crypto import get_random_string
from django.contrib.auth.models import User, Group, Permission
from oauth.models.base import UserLang, UserRecover, Profile, Branch, City
from oauth.libs.errors import *
from django.utils.translation import ugettext_lazy as _i18n
#  from core.libs.functions import sendsms
from django.core.mail import send_mail
from core.libs.functions import format_number_for_sms_send
from django.conf import settings
import logging
import yaml
import datetime
import _thread
import os
import json
import requests


default_log = logging.getLogger("default")
debug_log = logging.getLogger("debug")
log = logging.getLogger("request")
plog = logging.getLogger("request")


# All functions for CRUD. functions are structured accroding theirs work
# action[_quantity]_type[_by_criteria]
# ex: get_all_client_by_id, set_client_by_username, get_all_mode, get_user_by_id
# functions return list called result
# ##############################################################################
#
#
# ------------------------------------------------------------------------------
# Getters
# ------------------------------------------------------------------------------
def get_all_group():
    """ Return dictionary of group id and name as tuple"""
    return {_.id: _.name for _ in Group.objects.all()}


def get_user_groups(user):
    """ get all groups of given user as object """
    return [_.name for _ in user.groups.all()]

def check_user_group(my_user):
    livreur=[]
    for element in my_user :
        if element.groups.filter(name='livreur'):
            livreur.append(element)
    return livreur

def check_mission_state(mission,etat):
    this_mission=[]
    for element in mission :
        if element.voyage.etat_voyage==etat :
            this_mission.append(element)
    return this_mission

def get_group_permissions(group_name):
    """ get all permission of given group name. return list of permissions """
    group = Group.objects.filter(name=group_name)
    return [{p.codename: p.name for p in _} for _ in [
        p.permissions.all() for p in group]][0]


def get_user_permissions(user):
    """ get user permissions from group and direct assign """
    permissions_from_groups, permissions_direct = list(), None
    user_groups = get_user_groups(user)
    for _ in user_groups:
        permissions_from_groups.append(get_group_permissions(_))
    permissions_direct = [
        {x.codename: x.name} for x in Permission.objects.filter(user=user)][0]
    permissions_from_groups[0].update(permissions_direct)
    return permissions_from_groups[0]


def get_user_front_permissions(user):
    data = dict()
    profile = Profile.objects.get(user=user)
    return data


def get_user_lang(user):
    """ get user lang from front settings. """
    default_lang = 'fr'
    try:
        user_lang = UserLang.objects.get(user=user)
        default_lang = user_lang.lang
    except:
        pass
    return default_lang


def get_notification_content(user_id, code, kwargs=dict()):
    LANGUAGE = get_user_lang(user_id)
    CURRENT_LANG_DIR = os.path.join(settings.CONFIG_DIR, LANGUAGE)
    MESSAGES_FILE = os.path.join(CURRENT_LANG_DIR, settings.MESSAGES_FILE)

    with open(MESSAGES_FILE) as mf:
        messages = yaml.load(mf, Loader=yaml.SafeLoader)
    return messages[code].format(**kwargs)


def get_app_user_message(user_id, code):
    LANGUAGE = get_user_lang(user_id)
    CURRENT_LANG_DIR = os.path.join(settings.CONFIG_DIR, LANGUAGE)
    MESSAGES_FILE = os.path.join(CURRENT_LANG_DIR, settings.MESSAGES_FILE)

    with open(MESSAGES_FILE) as mf:
        messages = yaml.load(mf, Loader=yaml.SafeLoader)
    return messages


def get_app_users():
    data = list()
    # users = User.objects.filter(is_superuser=False).filter(is_active=True)
    users = User.objects.filter(is_superuser=False)
    for _ in users:
        user_groups = [g.name for g in _.groups.all()]
        # Only display user with group
        if bool(user_groups):
            data.append(
                {
                    'user': _,
                    'groups': [g.name for g in _.groups.all()],
                    'profile': Profile.objects.filter(user=_)
                }
            )
    return data


def get_app_user_detail(id):
    data = dict()
    user = User.objects.get(id=id)
    profile = Profile.objects.get(user=user)
    data['id'] = user.id
    data['first_name'] = user.first_name
    data['last_name'] = user.last_name
    data['email'] = user.email
    data['id_proof'] = profile.id_proof
    data['work_phone'] = profile.work_phone
    data['home_phone'] = profile.home_phone
    data['location'] = profile.location
    #  data['branch'] = profile.branch.name
    #  data['group'] = [g.name for g in user.groups.all()][0]
    data['branch'] = profile.branch.id if profile.branch else str()
    user_groups = [g.id for g in user.groups.all()]
    if bool(user_groups):
        data['group'] = user_groups[0]
    # data['group'] = [g.id for g in user.groups.all()][0]
    debug_log.debug("[?] Got data for ajax: {}".format(data))
    return data

def get_user_id(request):
    data=dict()
    user=User.objects.get(user=request.user)
    data['user'] = user
    return data

    



def get_branch_details(branch_id):
    data = dict()
    record = Branch.objects.filter(id=branch_id)
    if bool(record):
        data['id'] = record[0].id
        data['name'] = record[0].name
        data['phone'] = record[0].phone
        data['email'] = record[0].email
        data['address'] = record[0].address
        data['city'] = record[0].city.id
    return data


def get_user_profile(user_id):
    user = User.objects.get(id=user_id)
    user_profile = Profile.objects.get(user=user)
    return user_profile


def get_user_profile_v2(user):
    user_profile = Profile.objects.get(user=user)
    return user_profile


def show_user_permissions(user_id):
    user = User.objects.get(id=user_id)
    # data = [_.codename for _ in user.user_permissions.all()]
    data = [_.name for _ in user.user_permissions.all()]
    return json.dumps(data)


def get_user_branch(user_id):
    user = User.objects.get(id=user_id)
    user_profile = Profile.objects.get(user=user)
    return user_profile.branch


def get_user_branch_v2(user):
    profile = Profile.objects.get(user=user)
    return profile.branch


def get_all_users_of_group(group_name, exclude_users=None):
    if bool(exclude_users):
        return User.objects.filter(
            groups__name=group_name).exclude(id__in=exclude_users)
    return User.objects.filter(groups__name=group_name)


# ------------------------------------------------------------------------------
# Setters
# ------------------------------------------------------------------------------
def set_user_password(user_id, password):
    user = User.objects.get(id=user_id)
    user.password = make_password(password)
    return user.save()


def set_user_lang(user, lang):
    record = None
    try:
        record = UserLang.objects.get(user=user)
        record.lang = lang
        record.save()
        return lang
    except:
        record = UserLang.objects.create(**{'user': user, 'lang': lang})
        return record.lang


def set_recover_code(username):
    record = None
    check = check_username_in_user(username)
    if bool(check):
        recover_code = get_random_string(10)
        user = User.objects.get(username=username)
        profile = Profile.objects.get(user=user)
        phone_to_send = format_number_for_sms_send(profile.work_phone)
        if not check_user_in_recover(user):
            record = UserRecover.objects.create(
                **{'user': user, 'recover_code': recover_code})
        else:
            record = UserRecover.objects.filter(user=user).update(
                **{'recover_code': recover_code})
        sendsms(recover_code, phone_to_send)
    return record


def set_user_recover_password(username, password, recover_code):
    user = User.objects.get(username=username)
    record = UserRecover.objects.get(user=user)
    if bool(record.recover_code == recover_code):
        user.password = make_password(password)
        user.save()
        record.delete()
        return True
    return False


def set_branch(data, default_action=1, branch_id=None):
    record = None
    data['city'] = City.objects.get(id=data['city'])
    if default_action == 1:
        record = Branch.objects.create(**data)
    elif default_action == 2 and branch_id is not None:
        data = clean_dict(data)
        record = Branch.objects.filter(id=branch_id).update(**data)
        log.info("[+] got record: {}".format(record))
    return True


def set_app_user(data):
    debug_log.debug("[+] User create, got data: {}".format(data))
    username = "%s.%s" % (
        format_name_string(data['first_name'].lower()),
        format_name_string(data['last_name'].lower()))
    debug_log.debug("[+] username created: {}".format(username))
    password = get_random_string(length=10)
    debug_log.debug("[+] got password: {}".format(password))
    user = User.objects.create_user(
        username, data['email'], password, first_name=data['first_name'],
        last_name=data['last_name'], is_staff=True)
    UserLang.objects.create(**{'user': user})
    debug_log.debug("[+] finally, got user: {}".format(user))
    group = Group.objects.get(id=data['group'])
    debug_log.debug("[+] got group: {}".format(group))
    group.user_set.add(user)
    message_parts = {
        'user': "%s %s" % (data['first_name'], data['last_name']),
        'username': username,
        'password': password
    }
    debug_log.debug("[+] got message parts: {}".format(message_parts))
    message = get_notification_content(user.id, 800, message_parts)
    debug_log.debug("[+] got message: {}".format(message))
    message = get_notification_content(user.id, 800, message_parts)
    # Thread to handle Email sending
    try:
        default_log.info("[!] Starting thread to send Email")
        _thread.start_new_thread(
            handle_mail_sending, (message, data['email']))
    except:
        default_log.info("[x] Unable to start thread to send Mail")

    data.pop('first_name', None)
    data.pop('last_name', None)
    data.pop('email', None)
    data.pop('group', None)
    debug_log.debug("[+] got data: {}".format(data))
    if bool(data.get('branch', None)):
        data['branch'] = Branch.objects.get(id=data['branch'])
    profile = Profile.objects.filter(user=user).update(**data)
    debug_log.debug("[+] got profile: {}".format(profile))
    if profile is None:
        return True
    return False


def set_app_user_perms(data):
    user_id = data.pop('puser_id', None)
    user = User.objects.get(id=user_id)
    permissions = Permission.objects.filter(codename__in=data['permissions'])
    tmp_perms = user.user_permissions.all()

    # remove all permissions
    for _ in tmp_perms:
        user.user_permissions.remove(_)

    # assign new permissions
    for _ in permissions:
        user.user_permissions.add(_)
    user.save()

    return True



# ------------------------------------------------------------------------------
# Updaters
# ------------------------------------------------------------------------------
def update_app_user(data):
    debug_log.debug("[+] In update process, got data: {}".format(data))
    group = data['group']
    user = User.objects.get(id=int(data['user_id']))
    debug_log.debug("[+] user: {}".format(user))
    profile = Profile.objects.get(user=user)
    user.email = data['email']
    user.first_name = data['first_name']
    user.last_name = data['last_name']
    user.save()
    profile.work_phone = data['work_phone']
    profile.home_phone = data['home_phone']
    profile.id_proof = data['id_proof']
    profile.location = data['location']
    if bool(data.get('branch', None)):
        profile.branch = Branch.objects.get(id=data['branch'])
    profile.save()
    message_parts = {
        'user': "%s %s" % (data['first_name'], data['last_name']),
    }
    debug_log.debug("[+] got message parts: {}".format(message_parts))
    message = get_notification_content(user.id, 801, message_parts)
    debug_log.debug("[+] got message: {}".format(message))
    # Thread to handle Email sending
    try:
        default_log.info("[!] Starting thread to send SMS")
        _thread.start_new_thread(
            handle_mail_sending, (message, data['email']))
    except:
        default_log.info("[x] Unable to start thread to send Mail")

    del data
    # dynamically remove user from all groups
    groups = Group.objects.all()
    debug_log.debug("[+] all groups: {}".format(groups))
    for _ in groups:
        _.user_set.remove(user)
    user_group = Group.objects.get(id=group)
    user_group.user_set.add(user)
    return True


def disable_app_user(user_id):
    user = User.objects.get(id=user_id)
    user.is_active = False
    return user.save()


def enable_app_user(user_id):
    user = User.objects.get(id=user_id)
    user.is_active = True
    return user.save()


def disable_branch(branch_id):
    branch = Branch.objects.get(id=branch_id)
    branch.status = False
    return branch.save()


def enable_branch(branch_id):
    branch = Branch.objects.get(id=branch_id)
    branch.status = True
    return branch.save()


# ------------------------------------------------------------------------------
# Actions
# ------------------------------------------------------------------------------
def check_username_in_user(username):
    return User.objects.filter(username=username).exists()


def check_user_in_recover(user):
    return UserRecover.objects.filter(user=user).exists()


# ------------------------------------------------------------------------------
# Methods
# ------------------------------------------------------------------------------
def check_instance(model):
    """
        Checks if given model is a string. String model will be evaluated
        before each operation.
        we can get all data for model in _meta dict
    """
    if not isinstance(model, str):
        raise NotExpectedModel(model)
    try:
        eval(model)._meta.label_lower
        debug_log.debug('[!] function: check_instance. Got {}.' +
                        ' Attempting to get metadata of given model: {}'.format(
                            model, {k: v for k, v in
                                    eval(model)._meta.__dict__.items()}))
    except Exception as e:
        debug_log.debug("[x] Got Exception: {}".format(str(e)))
        raise ModelNotFound(model)


def clean_query_params(model, query_params):
    result = dict(query_params)
    default_log.info("[!] Starting with query_params: {} in model: {}".format(
        query_params, model))
    model_fields = [_.name for _ in eval(model)._meta.get_fields()]
    for _ in query_params.keys():
        if _ not in model_fields:
            default_log.info("[x] {} is not in model: {} fields. " +
                             "Removing it".format(_, model))
            del result[_]
    return result


def clean_dict(args):
    result = dict(args)
    for _ in args.keys():
        if not bool(args[_]):
            del result[_]
    return result


def format_time_AM_PM(str_time):
    period = str_time[-2:]
    hours, mins = int(
        str_time[:-2].split(":")[0]), int(str_time[:-2].split(":")[1])
    if period == 'PM':
        hours += 12
    return "%s:%s" % (hours, mins)


def format_time(str_time):
    hours, mins = int(str_time.split(":")[0]), int(str_time.split(":")[1])
    return datetime.time(hours, mins)


def format_name_string(string):
    return string.replace(' ', '.').replace('\'', '').replace('"', '')


def format_num(num):
    return "".join(num.split(" "))


#  def format_number_for_sms_send(str_number):
#      return "225%s" % format_num(str_number)
#
#
def format_date_time(date_time_obj):
    return date_time_obj.strftime("%d/%m/%Y - %H:%M")


def sendsms(message, to):
    url = "https://mks-microservices.tech/sms/send/"
    payload = {'_to': to, 'message': message}
    debug_log.debug(
        "[+] Requesting SMS Server for sending: {}".format(payload))
    query = requests.post(url, data=payload)
    return query.text


def handle_mail_sending(message, to, motive=_i18n('User Management')):
    debug_log.debug("[+] Sending Mail: %s" % message)
    return send_mail(
        "[%s]: %s" % (settings.APP_TITLE, motive),
        message, settings.EMAIL_HOST_USER, [to], fail_silently=True
    )


def isExists(model, params_dict):
    return eval(model).objects.filter(**params_dict).exists()
