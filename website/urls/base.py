#!/usr/bin/env python
# -*- coding: utf-8 -*-


from django.conf.urls import url
from django.conf.urls import include
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import frontspace as frontspace_urls
from . import userspace as userspace_urls
from . import waiting_page as waiting_page_urls 
from . import payement_state
#from .api import api
urlpatterns = [
    url(r'^', include(frontspace_urls)),
    path('wait/',include(waiting_page_urls)),
    path('payement_state/',include(payement_state)),
    path('back-office/',include(userspace_urls)),
    
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
