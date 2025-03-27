from django.conf import settings
from django.urls import include, path
from drf_spectacular.views import SpectacularAPIView

from django_auto_drf.auto_register import api_router_urls
from django_auto_drf.views import CustomSpectacularRedocView


def get_urlpatterns():
    urlpatterns = [
        path("api/", include(api_router_urls())),
    ]

    if settings.DEBUG:
        urlpatterns += [
            path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
            # path("api/docs/", SpectacularSwaggerView.as_view(url_name="schema"), name="swagger-ui"),
            path("api/docs/", CustomSpectacularRedocView.as_view(url_name="schema"), name="redoc"),
        ]
    return urlpatterns
