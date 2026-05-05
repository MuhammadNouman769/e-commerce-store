from django.contrib import admin
from apps.products.models import Product
from django.contrib import admin
from apps.products.models import ProductImage


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    inlines = [ProductImageInline]
    list_display = (
        "id",
        "title",
        "shop",
        "product_status",
        "is_featured",
        "is_new",
        "total_sold",
    )

    list_filter = (
        "product_status",
        "is_featured",
        "is_new",
        "is_on_sale",
    )

    search_fields = (
        "title",
        "shop__name",
        "brand",
    )

    filter_horizontal = (
        "categories",
    )

    readonly_fields = (
        "handle",
        "total_views",
        "total_sold",
        "average_rating",
    )

    fieldsets = (
        ("Basic Info", {
            "fields": ("shop", "title", "short_description", "description_html")
        }),
        ("Relations", {
            "fields": ("categories", "brand")
        }),
        ("product_Status", {
            "fields": ("product_status",)
        }),
        ("SEO", {
            "fields": ("meta_title", "meta_description", "meta_keywords")
        }),
        ("Flags", {
            "fields": ("is_featured", "is_best_seller", "is_new", "is_on_sale")
        }),
        ("Stats", {
            "fields": ("total_views", "total_sold", "average_rating")
        }),
    )


