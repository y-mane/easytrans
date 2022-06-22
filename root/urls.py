from django.conf.urls import url, include
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from oauth.urls import base as oauth_urls
from website.urls import base as website_urls
#from api.urls import base as api_urls
from sentry.urls import base as sentry_urls
from .api_ninja import api

urlpatterns = [
    path('admin-back-office/', admin.site.urls),
    #path('api/v1/', include(api_urls)),
    path('i18n/', include('django.conf.urls.i18n')),
    path('session_security/', include('session_security.urls')),
    path('oauth/', include(oauth_urls)),
    path('sentry/', include(sentry_urls)),
    path('', include(website_urls)),
    path('api-ninja/',api.urls)
    
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL,
                          document_root=settings.STATIC_ROOT)
