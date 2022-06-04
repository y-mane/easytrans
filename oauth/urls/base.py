#!/usr/bin/env python
# -*- coding: utf-8 -*-


from django.urls import path
# from django.conf.urls import include
from oauth.views import base
# from django.contrib.auth import urls as djauth

urlpatterns = [
    path('', base.index, name='auth_index'),
    path('login/', base.main_signin, name='auth_login'),
    path('login/google/', base.google_signin, name='auth_login_google'),
    path('login/facebook/', base.facebook_signin, name='auth_login_facebook'),
    path('login/linkedin/', base.linkedin_signin, name='auth_login_linkedin'),
    path('logout/', base.logout, name='auth_logout'),
    path('signup/', base.signup, name='auth_signup'),
    path('signup/process/', base.signup_process, name='auth_signup_process'),
    path('recover-start/',
        base.recover_password_first_step, name='auth_recover_first'),
    path('recover-end/',
        base.recover_password_second_step, name='auth_recover_second'),
    path('password/update/process/', base.password_edit_process,
        name='auth_password_edit_process'),
    path('profile/', base.profile, name='auth_profile'),
    path('profile/user/lang/',
        base.setting_language, name='auth_profile_lang'),
    path('profile/update/process/', base.profile_edit_process,
        name='auth_profile_edit_process'),
]
