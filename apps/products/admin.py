from django.contrib import admin
from .models import (
    Shop, Category, Product, ProductOption,
    ProductOptionValue, ProductVariant
)



# ===== Category Admin =====
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "shop", "parent", "position", "slug", "id")
    list_filter = ("shop", "parent")
    search_fields = ("name", "slug")
    ordering = ("shop", "position", "name")
    prepopulated_fields = {"slug": ("name",)}
    # Optional: Show children inline
    # inlines = [CategoryInline]

admin.site.register(Category, CategoryAdmin)


# ===== Product Option Value Inline =====
class ProductOptionValueInline(admin.TabularInline):
    model = ProductOptionValue
    extra = 1


# ===== Product Option Inline =====
class ProductOptionInline(admin.TabularInline):
    model = ProductOption
    extra = 1


# ===== Product Variant Inline =====
class ProductVariantInline(admin.TabularInline):
    model = ProductVariant
    extra = 1


# ===== Product Admin =====
class ProductAdmin(admin.ModelAdmin):
    list_display = ("title", "shop", "status", "published_at")
    list_filter = ("shop", "status", "categories")
    search_fields = ("title", "handle", "vendor")
    prepopulated_fields = {"handle": ("title",)}
    inlines = [ProductOptionInline, ProductVariantInline]
    filter_horizontal = ("categories",)  # nice UI for many-to-many

admin.site.register(Product, ProductAdmin)


# ===== Shop Admin =====
class ShopAdmin(admin.ModelAdmin):
    list_display = ("name", "domain", "description", "id")
    search_fields = ("name", "domain")

admin.site.register(Shop, ShopAdmin)


# ===== Product Option Admin =====
class ProductOptionAdmin(admin.ModelAdmin):
    list_display = ("name", "product", "position")
    inlines = [ProductOptionValueInline]

admin.site.register(ProductOption, ProductOptionAdmin)


# ===== Product Variant Admin =====
class ProductVariantAdmin(admin.ModelAdmin):
    list_display = ("sku", "product", "price", "compare_at_price", "weight", "position")
    list_filter = ("product",)
    search_fields = ("sku", "barcode", "option1", "option2", "option3")

admin.site.register(ProductVariant, ProductVariantAdmin)

