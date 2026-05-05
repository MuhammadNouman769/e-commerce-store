from django.contrib import admin
from apps.products.models import ProductVariant


@admin.register(ProductVariant)
class ProductVariantAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "product",
        "sku",
        "price",
        "stock_quantity",
        "is_in_stock",
    )

    list_filter = (
        "track_inventory",
        "allow_backorder",
    )

    search_fields = (
        "sku",
        "product__title",
    )