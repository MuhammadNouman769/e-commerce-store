"""
===============================================================
    URL configuration for core (Supply Chain / FootwareStore)
===============================================================
"""

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

#  NEW: drf-spectacular imports
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularSwaggerView,
    SpectacularRedocView
)


# ================= MAIN URLS =====================

urlpatterns = [
    path('admin/', admin.site.urls),

    # ===== App APIs =====
    path('', include('apps.main.urls')),  # Main app APIs
    path('api/', include('apps.users.urls')),  # Account APIs
    path('products/',include('apps.products.urls.product_urls')),
    path('shops/', include('apps.products.urls.shop_urls')),
    path('inventory/', include('apps.inventory_tracking.urls')),
    path('orders/', include('apps.order_fulfillment.urls')),
    path('shipments/', include('apps.shipment_monitoring.urls')),
    path('cart/', include('apps.cart.urls')),
    path('supply-chain/', include('apps.supplychain.urls')),

    # ===== API DOCUMENTATION (NEW SYSTEM) =====
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),

    path('api/swagger/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),

    path('api/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
]


# ============ Static & Media Serving (Development Only) ============

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0])