"""
=============== Imports ===============
"""
from django.contrib import admin
from .models import (
    Brand, Color, Size, Material, Technology, Style,
    Category, Product, ProductImage
)

"""
=============== Brand Admin ===============
"""
@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'logo')  # 'size_system' removed
    prepopulated_fields = {"slug": ("name",)}
    search_fields = ('name',)
    list_filter = ()  # Brand me koi size_system nahi, empty

"""
=============== Color Admin ===============
"""
@admin.register(Color)
class ColorAdmin(admin.ModelAdmin):
    list_display = ('name', 'hex_code')  # ensure ye model me exist kare
    search_fields = ('name',)

"""
=============== Size Admin ===============
"""
@admin.register(Size)
class SizeAdmin(admin.ModelAdmin):
    list_display = ('size', 'gender')  # 'value' replaced by 'size'
    list_filter = ('gender',)
    ordering = ('gender', 'size')      # 'value' replaced by 'size'
    search_fields = ('size',)

"""
=============== Material Admin ===============
"""
@admin.register(Material)
class MaterialAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

"""
=============== Technology Admin ===============
"""
@admin.register(Technology)
class TechnologyAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

"""
=============== Style Admin ===============
"""
@admin.register(Style)
class StyleAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

"""
=============== Category Admin ===============
"""
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'parent', 'slug')
    search_fields = ('name',)
    prepopulated_fields = {"slug": ("name",)}

"""
=============== ProductImage Inline ===============
"""
class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1
    readonly_fields = ('is_primary',)
    fields = ('image', 'alt_text', 'is_primary')

"""
=============== Product Admin ===============
"""
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        'title', 'category', 'brand', 'price', 'sale_price',
        'stock_quantity', 'is_active', 'is_featured'
    )
    list_filter = (
        'category', 'brand', 'is_active', 'is_featured',
        'is_new_arrival', 'is_best_seller', 'is_on_sale'
    )
    search_fields = ('title', 'sku')
    prepopulated_fields = {"slug": ("title",)}
    inlines = [ProductImageInline]
    filter_horizontal = ('colors', 'sizes', 'materials', 'styles', 'technologies')

"""
=============== ProductImage Admin ===============
"""
@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    list_display = ('product', 'alt_text', 'is_primary')
    list_filter = ('is_primary',)
