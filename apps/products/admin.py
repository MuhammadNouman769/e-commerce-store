from django.contrib import admin
from .models import (
    Shop, Category, Product, ProductOption,
    ProductOptionValue, ProductVariant, ProductImages   
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



class ProductImageInline(admin.TabularInline):
    model = ProductImages
    extra = 1


# ===== Product Admin =====
class ProductAdmin(admin.ModelAdmin):
    list_display = ("title", "shop", "display_categories", "status", "published_at")
    list_filter = ("shop", "status")  # Remove 'categories' from list_filter
    search_fields = ("title", "handle", "vendor")
    prepopulated_fields = {"handle": ("title",)}
    inlines = [ProductOptionInline, ProductVariantInline, ProductImageInline]
    filter_horizontal = ("categories",)  # nice UI for ManyToMany

    def display_categories(self, obj):
        return ", ".join([cat.name for cat in obj.categories.all()])
    display_categories.short_description = "Categories"
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

