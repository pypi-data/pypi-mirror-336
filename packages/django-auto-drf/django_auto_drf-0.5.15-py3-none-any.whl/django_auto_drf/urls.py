def get_urlpatterns(base_url=None):
    from django.conf import settings
    from django.urls import include, path

    from django_auto_drf.auto_register import api_router_urls
    from django_auto_drf.settings import DJANGO_AUTO_DRF_DEFAULT_BASE_URL, DJANGO_AUTO_DRF_DISABLE_SCHEMA_GENERATION
    baseurl = base_url or DJANGO_AUTO_DRF_DEFAULT_BASE_URL
    if not baseurl.endswith("/"):
        baseurl += "/"
    if baseurl.startswith("/"):
        baseurl = baseurl[1:]
    urlpatterns = [
        path(baseurl, include(api_router_urls())),
    ]

    if settings.DEBUG and not DJANGO_AUTO_DRF_DISABLE_SCHEMA_GENERATION:
        from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView

        urlpatterns += [
            path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
            path("api/docs/", SpectacularSwaggerView.as_view(url_name="schema"), name="swagger-ui"),
            path("api/redoc/", SpectacularRedocView.as_view(url_name="schema"), name="redoc"),
        ]
    return urlpatterns
