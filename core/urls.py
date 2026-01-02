""" ===============================================================
    URL configuration for core (Supply Chain / FootwareStore) project.

    The `urlpatterns` list routes URLs to views.
    For more information, see:
        https://docs.djangoproject.com/en/5.2/topics/http/urls/

    Author: Muhammad Nouman
    Version: v1.0
"""
""" ==============================
    Project URL Configuration
    Auto-generated API Docs using drf-yasg
================================ """

""" ================ Imports ================ """

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi


""" ================== Documentation Details ===================== """

schema_view = get_schema_view(
    openapi.Info(
        title="Supply Chain Management API",
        default_version='v1',
        description=(
            " **Auto-generated API documentation for the Supply Chain System.**\n\n"
            "### Modules Covered:\n"
            "-  User Management\n"
            "-  Inventory Tracking\n"
            "-  Order Fulfillment\n"
            "-  Shipment & Supplier Monitoring\n"
            "-  Product Management\n\n"
            "Use the Swagger or ReDoc interface to test API endpoints interactively."
        ),
        contact=openapi.Contact(email="nomannisar769@gmail.com"),
        license=openapi.License(name="MIT License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)


""" ================= MAIN URLS ===================== """

urlpatterns = [
    path('admin/', admin.site.urls),

    # ===== App APIs =====
    path('', include('apps.main.urls')),
    path('users/', include('apps.users.urls')),
    # path('api/orders/', include('apps.order_fulfillment.urls')),
    path('products/', include('apps.products.urls')),
    # path('api/suppliers/', include('apps.supplier_monitoring.urls')),
    # path('api/shipments/', include('apps.shipment_monitoring.urls')),

    # ===== API Documentation =====
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path('api/schema.json', schema_view.without_ui(cache_timeout=0), name='schema-json'),
]


""" ============ Static & Media Serving (Development Only) ============ """

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0])
