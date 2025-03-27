# 🚀 Django Auto DRF

**Automated API registration for Django Rest Framework**

Django Auto DRF is a powerful utility that **automatically registers ViewSets, Serializers, and Filters** for your
Django models. Skip the boilerplate and focus on your logic.

---

## 🌟 Features

- ✅ **Automatic API Registration**: No need to manually create ViewSets, Serializers, or Filters.
- ✅ **Multiple Endpoints per Model**: Register multiple APIs for the same model easily.
- ✅ **Custom Permissions & Pagination**: Customize permissions and pagination on each endpoint.
- ✅ **Django Admin-style Registration**: Just like `admin.site.register()` but for DRF.
- ✅ **Automatic OpenAPI Docs**: Swagger and Redoc supported out of the box.
- ✅ **Custom Extra Actions**: Add custom actions to your endpoints with decorators.
- ✅ **Autodiscovery**: Automatically imports `views.py`, `serializers.py`, and `filters.py` in each installed app.
- ✅ **Smart Defaults**: Auto-generates serializers and filtersets if not defined.
- ✅ **Config Inspection**: Retrieve registered configuration with `get_endpoint_config()`.

---

## 🚀 Installation

Install via pip:

```bash
pip install django-auto-drf
```

---

## ⚡ API Registration

### Registering Models

Use the `api_register_model()` function to register a model. You can optionally provide a custom endpoint, permissions,
pagination, etc.

```python
from django_auto_drf.registry import api_register_model
from .models import Product

api_register_model(Product)
```

### Registering Serializers or Filters

You can register a custom serializer or filterset using the same function as a decorator:

```python
@api_register_model(Product)
class ProductSerializer(ModelSerializer):
    class Meta:
        model = Product
        fields = "__all__"
```

### Adding Extra Actions

Use `api_register_action()` to add custom actions to your endpoints:

```python
from django_auto_drf.registry import api_register_action


@api_register_action(Product, methods=["post"])
def publish(request, pk=None):
    ...
```

### Access Configuration

You can inspect the registered configuration with:

```python
from django_auto_drf.registry import get_endpoint_config

config = get_endpoint_config(Product)
print(config)
```

---

## 📌 Quick Start

### 1. Add to `INSTALLED_APPS`

```python
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "rest_framework",
    "django_auto_drf",
]
```

### 2. Register a Model

```python
from django_auto_drf import register_api
from .models import Product

register_api(Product)
```

Now your API is live at:

```
GET /api/app_name/product/
POST /api/app_name/product/
PUT /api/app_name/product/{id}/
DELETE /api/app_name/product/{id}/
```

---

## 📖 Advanced Usage

### Custom Endpoint

```python
register_api(Product, endpoint="shop/products")
```

### Multiple Endpoints for the Same Model

```python
from rest_framework.permissions import IsAuthenticated, AllowAny


@register_api(Product, permissions=[IsAuthenticated])
class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()


@register_api(Product, endpoint="shop/products", permissions=[AllowAny])
class PublicProductViewSet(ModelViewSet):
    queryset = Product.objects.filter(is_published=True)
```

### Custom Pagination

```python
register_api(Product, paginate_by=50)
```

### Add Extra Actions

```python
@register_api(Product)
class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()

    @action(detail=True, methods=["post"])
    def publish(self, request, pk=None):
        ...
```

---

## 📜 Automatic Documentation

If `DEBUG=True` and schema generation is not disabled, visit:

- Swagger UI: `http://localhost:8000/api/docs/`
- Redoc UI: `http://localhost:8000/api/redoc/`

No need to configure, it's automatic!

---

## 🎯 Why Django Auto DRF?

- ⏳ Save development time
- 📈 Scale with multiple apps and endpoints
- ✅ DRY principle in action
- ⚙️ Fully customizable but easy to get started

---

## 🔧 Settings (Optional)

| Setting                                   | Description                           | Default           |
|-------------------------------------------|---------------------------------------|-------------------|
| DJANGO_AUTO_DRF_DEFAULT_VIEWSET           | Base class for ViewSets               | `ModelViewSet`    |
| DJANGO_AUTO_DRF_DEFAULT_SERIALIZER        | Base class for Serializers            | `ModelSerializer` |
| DJANGO_AUTO_DRF_DEFAULT_FILTERSET         | Base class for FilterSets             | `FilterSet`       |
| DJANGO_AUTO_DRF_DEFAULT_BASE_URL          | Root path for APIs                    | "api/"            |
| DJANGO_AUTO_DRF_DISABLE_SCHEMA_GENERATION | Disable Swagger/Redoc when DEBUG=True | `False`           |

---

## 🛠️ Development & Contribution

1. Clone:
   ```bash
   git clone https://github.com/wolfmc3/django-auto-drf.git
   cd django-auto-drf
   ```
2. Virtual env:
   ```bash
   python -m venv venv
   source venv/bin/activate  # Windows: venv\Scripts\activate
   ```
3. Install:
   ```bash
   pip install -r requirements.txt
   ```
4. Run tests:
   ```bash
   python manage.py test
   ```

---

## 🔗 Links

- 📄 [Docs](https://github.com/wolfmc3/django-auto-drf/wiki)
- ✨ [Issues](https://github.com/wolfmc3/django-auto-drf/issues)
- 🌐 [Source](https://github.com/wolfmc3/django-auto-drf)

