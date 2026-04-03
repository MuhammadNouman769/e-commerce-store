# # apps/products/admin.py
# from django.contrib import admin
# from django.utils.html import format_html
# from django.utils.safestring import mark_safe
# from .models import (
#     Shop, Category, Product, ProductImage,
#     ProductOption, ProductOptionValue, ProductVariant
# )

# # =====================================
# # Inlines
# # =====================================

# class ProductImageInline(admin.TabularInline):
#     model = ProductImage
#     extra = 3
#     fields = ('images', 'alt_text', 'position', 'image_preview')
#     readonly_fields = ('image_preview',)
#     ordering = ('position',)

#     def image_preview(self, obj):
#         if obj.images:
#             return format_html(
#                 '<img src="{}" style="max-height: 80px; border-radius: 6px; border: 1px solid #ddd;" />',
#                 obj.images.url
#             )
#         return mark_safe('<span style="color: #999;">No Image</span>')
#     image_preview.short_description = "Preview"


# class ProductOptionValueInline(admin.TabularInline):
#     model = ProductOptionValue
#     extra = 3
#     fields = ('value', 'position')
#     ordering = ('position',)


# class ProductOptionInline(admin.TabularInline):
#     model = ProductOption
#     extra = 1
#     fields = ('name', 'position')
#     ordering = ('position',)
#     inlines = [ProductOptionValueInline]


# class ProductVariantInline(admin.TabularInline):
#     model = ProductVariant
#     extra = 1
#     fields = (
#         'sku', 'barcode', 'price', 'compare_at_price',
#         'weight', 'option1', 'option2', 'option3', 'position'
#     )
#     autocomplete_fields = ('option1', 'option2', 'option3')
#     ordering = ('position',)


# # =====================================
# # Category Admin
# # =====================================
# @admin.register(Category)
# class CategoryAdmin(admin.ModelAdmin):
#     list_display = ('name', 'shop', 'parent', 'position', 'slug', 'get_full_path')
#     list_filter = ('shop', 'parent')
#     search_fields = ('name', 'slug')
#     ordering = ('shop', 'position', 'name')
#     prepopulated_fields = {'slug': ('name',)}
#     list_select_related = ('shop', 'parent')

#     def get_full_path(self, obj):
#         return obj.get_full_path()
#     get_full_path.short_description = "Full Path"
#     get_full_path.admin_order_field = 'position'


# # =====================================
# # Shop Admin
# # =====================================
# @admin.register(Shop)
# class ShopAdmin(admin.ModelAdmin):
#     list_display = ('name', 'domain', 'owner', 'created_at')
#     search_fields = ('name', 'domain', 'owner__email', 'owner__phone')
#     list_select_related = ('owner',)
#     readonly_fields = ('created_at', 'updated_at')


# # =====================================
# # Product Admin (Most Important)
# # =====================================
# @admin.register(Product)
# class ProductAdmin(admin.ModelAdmin):
#     list_display = (
#         'title', 'shop', 'status', 'vendor',
#         'display_categories', 'has_variants', 'created_at'
#     )
#     list_filter = ('shop', 'status', 'vendor', 'product_type', 'created_at')
#     search_fields = ('title', 'handle', 'vendor', 'description_html')
#     prepopulated_fields = {'handle': ('title',)}
#     filter_horizontal = ('categories',)
#     list_select_related = ('shop',)
#     readonly_fields = ('created_at', 'updated_at', 'handle')
#     date_hierarchy = 'created_at'

#     fieldsets = (
#         ("Basic Information", {
#             'fields': ('title', 'handle', 'shop', 'description_html'),
#             'classes': ('collapse',)
#         }),
#         ("Organization & Classification", {
#             'fields': ('vendor', 'product_type', 'categories'),
#         }),
#         ("Status & Publishing", {
#             'fields': ('status', 'published_at'),
#         }),
#         ("System Information", {
#             'fields': ('created_at', 'updated_at'),
#             'classes': ('collapse',)
#         }),
#     )

#     inlines = [
#         ProductImageInline,      # Gallery First (Visual)
#         ProductOptionInline,     # Options
#         ProductVariantInline,    # Variants
#     ]

#     def display_categories(self, obj):
#         cats = obj.categories.all()[:5]
#         return ", ".join([cat.name for cat in cats]) + ("..." if obj.categories.count() > 5 else "")
#     display_categories.short_description = "Categories"

#     def has_variants(self, obj):
#         count = obj.variants.count()
#         return format_html(
#             '<span style="color: {};">{} Variant{}</span>',
#             'green' if count > 0 else 'orange',
#             count,
#             's' if count != 1 else ''
#         )
#     has_variants.short_description = "Variants"
#     has_variants.admin_order_field = 'variants__count'  # if you add annotation

#     # Optional: Custom CSS for better look
#     class Media:
#         css = {
#             'all': ('admin/css/custom_admin.css',)  # you can create this file later
#         }


# # =====================================
# # ProductOption Admin
# # =====================================
# @admin.register(ProductOption)
# class ProductOptionAdmin(admin.ModelAdmin):
#     list_display = ('name', 'product', 'position')
#     list_filter = ('product__shop',)
#     search_fields = ('name', 'product__title')
#     ordering = ('product', 'position')
#     inlines = [ProductOptionValueInline]


# # =====================================
# # ProductOptionValue Admin
# # =====================================
# @admin.register(ProductOptionValue)
# class ProductOptionValueAdmin(admin.ModelAdmin):
#     list_display = ('value', 'option', 'position')
#     list_filter = ('option__product__shop', 'option')
#     search_fields = ('value',)
#     ordering = ('option', 'position')


# # =====================================
# # ProductVariant Admin
# # =====================================
# @admin.register(ProductVariant)
# class ProductVariantAdmin(admin.ModelAdmin):
#     list_display = (
#         'product', 'sku', 'barcode', 'price',
#         'compare_at_price', 'get_options_display', 'position'
#     )
#     list_filter = ('product__shop', 'product')
#     search_fields = ('sku', 'barcode', 'product__title')
#     autocomplete_fields = ('product', 'option1', 'option2', 'option3')
#     ordering = ('product', 'position')

#     def get_options_display(self, obj):
#         options = []
#         if obj.option1: options.append(obj.option1.value)
#         if obj.option2: options.append(obj.option2.value)
#         if obj.option3: options.append(obj.option3.value)
#         return " / ".join(options) or "-"
#     get_options_display.short_description = "Options"

