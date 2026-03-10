from django.contrib import admin
from django.utils.html import format_html
from .models import (
    Shop,
    Category,
    Product,
    ProductOption,
    ProductOptionValue,
    ProductVariant,
    ProductImages
)

# ===============================
# Category Admin
# ===============================
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "shop", "parent", "position", "slug", "id")
    list_filter = ("shop",)
    search_fields = ("name", "slug")
    ordering = ("shop", "position")
    prepopulated_fields = {"slug": ("name",)}
    list_select_related = ("shop", "parent")

    def get_queryset(self, request):
        return super().get_queryset(request).select_related("shop", "parent")


# ===============================
# Product Image Inline
# ===============================
class ProductImageInline(admin.TabularInline):
    model = ProductImages
    extra = 1
    readonly_fields = ("image_preview",)

    def image_preview(self, obj):
        if obj.images:
            return format_html(
                '<img src="{}" width="80" style="border-radius:5px;"/>', obj.images.url
            )
        return "-"
    image_preview.short_description = "Preview"


# ===============================
# Product Option Value Inline
# ===============================
class ProductOptionValueInline(admin.TabularInline):
    model = ProductOptionValue
    extra = 1


# ===============================
# Product Option Inline
# ===============================
class ProductOptionInline(admin.TabularInline):
    model = ProductOption
    extra = 1


# ===============================
# Product Variant Inline
# ===============================
class ProductVariantInline(admin.TabularInline):
    model = ProductVariant
    extra = 1
    fields = (
        "sku",
        "barcode",
        "price",
        "compare_at_price",
        "weight",
        "option1",
        "option2",
        "option3",
        "position",
    )
    autocomplete_fields = ("option1", "option2", "option3")


# ===============================
# Product Admin
# ===============================
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "shop",
        "status",
        "published_at",
        "display_categories",
    )
    list_filter = ("shop", "status", "created_at")
    search_fields = ("title", "handle", "vendor")
    prepopulated_fields = {"handle": ("title",)}
    filter_horizontal = ("categories",)
    readonly_fields = ("created_at", "updated_at")
    inlines = [
        ProductImageInline,
        ProductOptionInline,
        ProductVariantInline,
    ]
    list_select_related = ("shop",)

    fieldsets = (
        ("Basic Information", {"fields": ("title", "handle", "description_html", "shop")}),
        ("Organization", {"fields": ("vendor", "product_type", "categories")}),
        ("Status", {"fields": ("status", "published_at")}),
        ("System Information", {"fields": ("created_at", "updated_at")}),
    )

    def display_categories(self, obj):
        return ", ".join(cat.name for cat in obj.categories.all())
    display_categories.short_description = "Categories"


# ===============================
# Shop Admin
# ===============================
@admin.register(Shop)
class ShopAdmin(admin.ModelAdmin):
    list_display = ("name", "domain", "id")
    search_fields = ("name", "domain")


# ===============================
# Product Option Admin
# ===============================
@admin.register(ProductOption)
class ProductOptionAdmin(admin.ModelAdmin):
    list_display = ("name", "product", "position")
    search_fields = ("name",)
    inlines = [ProductOptionValueInline]


# ===============================
# Product Option Value Admin
# ===============================
@admin.register(ProductOptionValue)
class ProductOptionValueAdmin(admin.ModelAdmin):
    list_display = ("value", "option", "position")
    search_fields = ("value",)


# ===============================
# Product Variant Admin
# ===============================
@admin.register(ProductVariant)
class ProductVariantAdmin(admin.ModelAdmin):
    list_display = ("sku", "product", "price", "compare_at_price", "weight", "position")
    list_filter = ("product",)
    search_fields = ("sku", "barcode")
    autocomplete_fields = ("product", "option1", "option2", "option3")