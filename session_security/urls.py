try:
    from django.conf.urls import url
except ImportError:
    from django.conf.urls.defaults import url

from .views import PingView

urlpatterns = [
    url(
        'ping/$',
        PingView.as_view(),
        name='session_security_ping',
    )
]
