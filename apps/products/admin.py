from django.contrib import admin
from .models import (
    Brand, Color, Size, Material, Technology, Style,
    Category, Product, ProductImage
)

@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ('name', 'size_system', 'slug', 'logo')
    prepopulated_fields = {"slug": ("name",)}
    search_fields = ('name',)

@admin.register(Color)
class ColorAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

@admin.register(Size)
class SizeAdmin(admin.ModelAdmin):
    list_display = ('value', 'gender')
    list_filter = ('gender',)
    ordering = ('gender', 'value')
    search_fields = ('value',)

@admin.register(Material)
class MaterialAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

@admin.register(Technology)
class TechnologyAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

@admin.register(Style)
class StyleAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'parent', 'slug')
    search_fields = ('name',)
    prepopulated_fields = {"slug": ("name",)}

class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1
    readonly_fields = ('is_primary',)
    fields = ('image', 'alt_text', 'is_primary')

@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    list_display = ('product', 'alt_text', 'is_primary')
    list_filter = ('is_primary',)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        'title', 'category', 'brand', 'price', 'sale_price',
        'stock_quantity', 'is_active', 'is_featured',
    )
    list_filter = (
        'category', 'brand', 'is_active', 'is_featured',
        'is_new_arrival', 'is_best_seller', 'is_on_sale'
    )
    search_fields = ('title', 'sku')
    prepopulated_fields = {"slug": ("title",)}
    inlines = [ProductImageInline]
    filter_horizontal = ('colors', 'sizes', 'materials', 'styles', 'technologies')

