from importlib import import_module

from django.core.exceptions import ImproperlyConfigured
from django_filters.rest_framework import FilterSet
from rest_framework.serializers import ModelSerializer
from rest_framework.viewsets import ModelViewSet

from django_auto_drf.core import EndpointConfig

api_registry = dict()


def api_register_model(model, endpoint=None):
    """
    Decorator for automatic registration of ViewSets, Serializers, and FilterSets.
    """
    model_name = model.__name__.lower()
    app_label = model._meta.app_label
    endpoint_path = endpoint or f"{app_label}/{model_name}"
    if endpoint_path not in api_registry:
        api_registry[endpoint_path] = EndpointConfig(endpoint_path, model._meta.label)

    def decorator(cls=None):
        if cls is None:
            return api_registry[endpoint_path]

        # Ottieni l'istanza corrente del registro da api_registry
        registry_entry = api_registry[endpoint_path]

        # Controlla e aggiorna i campi appropriati nella classe APIRegistryEntry
        if issubclass(cls, ModelViewSet):
            registry_entry.viewset_class = cls
        elif issubclass(cls, ModelSerializer):
            registry_entry.serializer_class = cls
        elif issubclass(cls, FilterSet):
            registry_entry.filterset_class = cls
        return cls

    return decorator


def api_register_action(model, endpoint=None, detail=True, methods=None):
    if methods is None:
        methods = ['get']
    model_name = model.__name__.lower()
    app_label = model._meta.app_label
    endpoint_path = endpoint or f"{app_label}/{model_name}"
    if endpoint_path not in api_registry:
        api_registry[endpoint_path] = EndpointConfig(endpoint_path, model._meta.label)

    def decorator(func):
        registry_entry = api_registry[endpoint_path]
        registry_entry.add_action(func.__name__, func, detail=detail, methods=methods)

        return func

    return decorator


def get_endpoint_config(model, endpoint=None):
    model_name = model.__name__.lower()
    app_label = model._meta.app_label
    endpoint_path = endpoint or f"{app_label}/{model_name}"
    return api_registry[endpoint_path]


def load_class_from_module(module_path, class_name):
    """
    Tenta di caricare una classe specifica da un modulo dato.
    Se il modulo o la classe non esistono, restituisce None.

    :param module_path: Percorso del modulo (es. 'myapp.serializers')
    :param class_name: Nome della classe da importare (es. 'DefaultModelSerializer')
    :return: La classe se trovata, altrimenti None
    """
    try:
        module = import_module(module_path)
        return getattr(module, class_name, None)
    except (ModuleNotFoundError, ImproperlyConfigured, AttributeError):
        return None


def discovery_api_models(app, exclude_models=None):
    """
    Iterates through the app's models and registers them with `api_register_model`,
    attempting to load Default<ModelName>Serializer and Default<ModelName>FilterSet
    for each model and register them if they exist.
    """
    # Normalizza le etichette dei modelli da escludere in lowercase
    exclude_models = [model.lower() for model in (exclude_models or [])]

    # Cicla sui modelli registrati nell'app (self.get_models include solo quelli dell'app corrente)
    for model in app.get_models():
        model_label = model._meta.label_lower
        if model_label in exclude_models:
            continue

        # Registra il modello
        api_register_model(model)

        # Ottieni il nome del modello
        model_name = model.__name__

        # Tenta di caricare e registrare il serializer e il filterset
        serializer_class_name = f"Default{model_name}Serializer"
        filterset_class_name = f"Default{model_name}FilterSet"

        # Usa la funzione generica per caricare classi dai moduli
        serializer_class = load_class_from_module(f"{app.name}.serializers", serializer_class_name)
        filterset_class = load_class_from_module(f"{app.name}.filters", filterset_class_name)

        # Registra il serializer se esiste
        if serializer_class:
            api_register_model(model)(serializer_class)

        # Registra il filterset se esiste
        if filterset_class:
            api_register_model(model)(filterset_class)
