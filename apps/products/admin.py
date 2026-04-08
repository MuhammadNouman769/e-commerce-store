# apps/products/admin.py
from django.contrib import admin
from django.utils.html import format_html
from .models import (
    Shop, Category, Product, ProductImage,
    ProductOption, ProductOptionValue, ProductVariant
)

# ==============================
# Inlines
# ==============================
class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 3
    fields = ('image', 'alt_text', 'position', 'image_preview')
    readonly_fields = ('image_preview',)
    ordering = ('position',)

    def image_preview(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" style="max-height: 80px; border-radius: 6px; border: 1px solid #ddd;" />',
                obj.image.url
            )
        return "No Image"
    image_preview.short_description = "Preview"


class ProductOptionValueInline(admin.TabularInline):
    model = ProductOptionValue
    extra = 3
    fields = ('value', 'position')
    ordering = ('position',)


class ProductOptionInline(admin.TabularInline):
    model = ProductOption
    extra = 1
    fields = ('name', 'position')
    ordering = ('position',)
    inlines = [ProductOptionValueInline]


class ProductVariantInline(admin.TabularInline):
    model = ProductVariant
    extra = 1
    fields = ('sku', 'barcode', 'price', 'compare_at_price', 'option1', 'option2', 'option3', 'position')
    autocomplete_fields = ('option1', 'option2', 'option3')
    ordering = ('position',)


# ==============================
# Shop Admin
# ==============================
@admin.register(Shop)
class ShopAdmin(admin.ModelAdmin):
    list_display = ('name', 'owner', 'created_at')
    search_fields = ('name', 'owner__email', 'owner__phone')
    readonly_fields = ('created_at', 'updated_at')
    list_select_related = ('owner',)


# ==============================
# Category Admin
# ==============================
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'parent', 'position', 'get_full_path')
    list_filter = ('parent',)
    search_fields = ('name',)
    ordering = ('position', 'name')

    def get_full_path(self, obj):
        return obj.get_full_path()
    get_full_path.short_description = "Full Path"
    get_full_path.admin_order_field = 'position'


# ==============================
# Product Admin
# ==============================
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('title', 'shop', 'status', 'display_categories', 'has_variants', 'created_at')
    list_filter = ('shop', 'status', 'created_at')
    search_fields = ('title', 'description_html')
    filter_horizontal = ('categories',)
    readonly_fields = ('created_at', 'updated_at')
    date_hierarchy = 'created_at'

    fieldsets = (
        ("Basic Information", {
            'fields': ('title', 'shop', 'description_html'),
        }),
        ("Organization & Classification", {
            'fields': ('categories',),
        }),
        ("Status & Publishing", {
            'fields': ('status',),
        }),
        ("System Information", {
            'fields': ('created_at', 'updated_at'),
        }),
    )

    inlines = [
        ProductImageInline,
        ProductOptionInline,
        ProductVariantInline,
    ]

    def display_categories(self, obj):
        cats = obj.categories.all()[:5]
        return ", ".join([cat.name for cat in cats]) + ("..." if obj.categories.count() > 5 else "")
    display_categories.short_description = "Categories"

    def has_variants(self, obj):
        count = obj.variants.count()
        return format_html(
            '<span style="color: {};">{} Variant{}</span>',
            'green' if count > 0 else 'orange',
            count,
            's' if count != 1 else ''
        )
    has_variants.short_description = "Variants"


# ==============================
# ProductOption Admin
# ==============================
@admin.register(ProductOption)
class ProductOptionAdmin(admin.ModelAdmin):
    list_display = ('name', 'product', 'position')
    ordering = ('product', 'position')
    inlines = [ProductOptionValueInline]


# ==============================
# ProductOptionValue Admin
# ==============================
@admin.register(ProductOptionValue)
class ProductOptionValueAdmin(admin.ModelAdmin):
    list_display = ('value', 'option', 'position')
    search_fields = ('value',)
    ordering = ('option', 'position')


# ==============================
# ProductVariant Admin
# ==============================
@admin.register(ProductVariant)
class ProductVariantAdmin(admin.ModelAdmin):
    list_display = ('product', 'sku', 'barcode', 'price', 'compare_at_price', 'get_options_display', 'position')
    list_filter = ('product',)
    search_fields = ('sku', 'barcode', 'product__title')
    autocomplete_fields = ('option1', 'option2', 'option3')
    ordering = ('product', 'position')

    def get_options_display(self, obj):
        values = [opt.value for opt in [obj.option1, obj.option2, obj.option3] if opt]
        return " / ".join(values) if values else "-"
    get_options_display.short_description = "Options"