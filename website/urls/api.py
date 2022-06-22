from unicodedata import name
from django.urls import path
from django.conf.urls import include
from django.conf import settings
from django.conf.urls.static import static
from website.views import api

urlpatterns = [
    path('',api.urls),

]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(
        settings.STATIC_URL, document_root=settings.STATIC_ROOT)
