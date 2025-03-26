from collections import OrderedDict

from django.apps import apps
from django.utils.module_loading import import_string
from drf_spectacular.openapi import AutoSchema
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

from django_auto_drf.settings import DJANGO_AUTO_DRF_DEFAULT_FILTERSET, DJANGO_AUTO_DRF_DEFAULT_SERIALIZER, \
    DJANGO_AUTO_DRF_DEFAULT_VIEWSET

DefaultViewSet = import_string(DJANGO_AUTO_DRF_DEFAULT_VIEWSET)
DefaultSerializer = import_string(DJANGO_AUTO_DRF_DEFAULT_SERIALIZER)
DefaultFilterSet = import_string(DJANGO_AUTO_DRF_DEFAULT_FILTERSET)


class EndpointConfig:
    def __init__(self, enpoint, model):
        self._endpoint = enpoint
        self.model_label = model
        self.viewset_class = None
        self.serializer_class = None
        self.filterset_class = None
        self.permissions = None
        self.paginate_by = None
        self.extra_actions = []

    def get_model_object(self):
        return apps.get_model(self.model_label)

    def get_base_name(self):
        return self._endpoint.replace("/", "-")

    def get_class_base_name(self):
        names = self._endpoint.split("/")
        return "".join(map(lambda x: x.capitalize(), names))

    def get_viewset(self):
        # Configura il serializer se non è definito
        model_obj = self.get_model_object()
        if not self.serializer_class:
            class AutoSerializer(DefaultSerializer):
                class Meta:
                    model = model_obj
                    fields = '__all__'

            AutoSerializer.__name__ = f"{self.get_class_base_name()}Serializer"
            self.serializer_class = AutoSerializer

        # Configura il filterset se non è definito
        if not self.filterset_class:
            class AutoFilterSet(DefaultFilterSet):
                class Meta:
                    model = model_obj
                    fields = '__all__'

            self.filterset_class = AutoFilterSet

        # Configura il viewset se non è definito
        if not self.viewset_class:
            class AutoViewSet(DefaultViewSet):
                queryset = model_obj.objects.all()
                permission_classes = self.permissions if self.permissions else []
                schema = AutoSchema()  # Uso dello schema automatico per DRF

            viewset_class = AutoViewSet
        else:
            viewset_class = self.viewset_class

        if not getattr(viewset_class, "serializer_class", None):
            viewset_class.serializer_class = self.serializer_class
        if not getattr(viewset_class, "filterset_class", None):
            viewset_class.filterset_class = self.filterset_class
        if (not getattr(viewset_class, "pagination_class", None)) and self.paginate_by:
            viewset_class.pagination_class = StandardResultsSetPaginationBuilder(self.paginate_by)

        for name, method in self.extra_actions:
            setattr(viewset_class, name, method)

        return viewset_class

    def add_action(self, name, func, detail=True, methods=None):
        if methods is None:
            methods = ['get']
        from rest_framework.decorators import action

        method = action(detail=detail, methods=methods)(func)
        method.__name__ = name
        self.extra_actions.append((name, method))

    def __repr__(self):
        return f"APIRegistryEntry(endpoint={self._endpoint}, basename={self.get_base_name()}, model={self.model_label}, viewset={self.viewset_class}, serializer={self.serializer_class}, " \
               f"filterset={self.filterset_class}, permissions={self.permissions}, paginate_by={self.paginate_by})"


def StandardResultsSetPaginationBuilder(paginate_by):
    class StandardResultsSetPagination(PageNumberPagination):
        page_size = paginate_by
        page_size_query_param = 'page_size'
        max_page_size = 100000

        def get_page_size(self, request):
            page_size = super().get_page_size(request)
            return page_size

        def get_paginated_response(self, data):
            return Response(OrderedDict([
                ('count', self.page.paginator.count),
                ('page', self.page.number),
                ('per_page', self.get_page_size(self.request)),
                ('results', data)
            ]))

    return StandardResultsSetPagination
