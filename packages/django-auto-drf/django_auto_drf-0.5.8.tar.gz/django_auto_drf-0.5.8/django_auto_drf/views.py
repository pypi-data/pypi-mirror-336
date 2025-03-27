from drf_spectacular.openapi import AutoSchema
from drf_spectacular.views import SpectacularRedocView


class CustomSpectacularRedocView(SpectacularRedocView):
    schema = AutoSchema()
