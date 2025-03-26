# 🚀 Django Auto DRF

**Automated API registration for Django Rest Framework**

Django Auto DRF is a powerful tool that **automatically registers ViewSets, Serializers, and Filters** for your Django
models. No more manual API configuration – just register your model, and Django Auto DRF will do the rest!

---

## 🌟 Features

✅ **Automatic API Registration** – No need to manually create ViewSets, Serializers, or Filters.  
✅ **Multiple Endpoints per Model** – Easily register multiple APIs for the same model with different endpoints.  
✅ **Custom Permissions** – Define authentication and permissions directly in the decorator.  
✅ **Django Admin-style Registration** – Just use `@register_api` like Django Admin’s `admin.site.register()`.  
✅ **Automatic OpenAPI Documentation** – Swagger and Redoc support out-of-the-box.  
✅ **Full Django Rest Framework (DRF) Integration** – Works seamlessly with DRF, Django Filters, and Django ORM.

---

## 🚀 Installation

Install via **pip**:

```bash
pip install django-auto-drf
```

---

## 📌 Quick Start

### **1️⃣ Add `django-auto-drf` to your `INSTALLED_APPS`** in `settings.py`:

```python
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "rest_framework",
    "django_auto_drf",  # Add this
]
```

### **2️⃣ Register a model** (No ViewSet, Serializer, or FilterSet required!)

```python
from django_auto_drf import register_api
from .models import Product

register_api(Product)  # This will create a full CRUD API at /api/app_name/product/
```

### **3️⃣ Run your server and test your API!**

```bash
python manage.py runserver
```

Your API is now available at the following endpoints:
GET /api/app_name/product/ POST /api/app_name/product/ PUT /api/app_name/product/{id}/ DELETE
/api/app_name/product/{id}/
---

## 📖 Advanced Usage

### **Register with a custom endpoint**

```python
register_api(Product, endpoint="shop/products")
```

📌 **Your API is now available at:**

GET /api/shop/products/

### **Register multiple APIs for the same model**

```python
from rest_framework.permissions import IsAuthenticated, AllowAny


@register_api(Product, permissions=[IsAuthenticated])
class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()


@register_api(Product, endpoint="shop/products", permissions=[AllowAny])
class PublicProductViewSet(ModelViewSet):
    queryset = Product.objects.filter(is_published=True)
```

📌 **Now you have two endpoints:**

- `/api/app_name/product/` (Requires authentication)
- `/api/shop/products/` (Public access)

---

## 📜 Auto-Generated API Documentation

Django Auto DRF automatically generates **Swagger UI and Redoc documentation**.  
Just add this to your `urls.py`:

```python
from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView

urlpatterns = [
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path("api/docs/", SpectacularSwaggerView.as_view(url_name="schema"), name="swagger-ui"),
    path("api/redoc/", SpectacularRedocView.as_view(url_name="schema"), name="redoc"),
]
```

📌 **Now access your documentation at:**

- **Swagger UI** → `http://localhost:8000/api/docs/`
- **Redoc UI** → `http://localhost:8000/api/redoc/`

---

## 🎯 Why Use Django Auto DRF?

- **Saves time** – No need to manually create ViewSets and Serializers.
- **Scales easily** – Works with large projects with multiple apps.
- **Reduces errors** – Ensures consistency across all APIs.
- **Fully customizable** – Supports custom ViewSets, Serializers, and Filters when needed.

---

## 🔧 Development & Contribution

1. Clone the repository:
   ```bash
   git clone https://github.com/wolfmc3/django-auto-drf.git
   cd django-auto-drf
   ```
2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # Windows: venv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Run tests:
   ```bash
   python manage.py test
   ```