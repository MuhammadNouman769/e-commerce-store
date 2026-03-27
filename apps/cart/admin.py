
# =====================================
# Register Cart Models (from your other file)
# =====================================
from .models import Address, Cart, CartItem, ShippingAddress   # Update path if needed
from django.contrib import admin

@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'country', 'province', 'city', 'street', 'created_at')
    list_filter = ('country', 'province')
    search_fields = ('street', 'user__email', 'user__phone')
    list_select_related = ('user', 'country', 'province', 'city')


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'total_items', 'created_at', 'updated_at')
    list_filter = ('created_at',)
    search_fields = ('user__email', 'user__phone')
    list_select_related = ('user',)
    readonly_fields = ('created_at', 'updated_at')

    def total_items(self, obj):
        return obj.items.count()
    total_items.short_description = "Items"


@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'cart', 'product', 'variant_display', 'quantity', 'price', 'total_price', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('product_name', 'cart__user__email')
    list_select_related = ('cart', 'cart__user', 'product', 'variant')

    def variant_display(self, obj):
        return obj.variant if obj.variant else "-"
    variant_display.short_description = "Variant"

    def total_price(self, obj):
        return obj.total_price
    total_price.short_description = "Total"


@admin.register(ShippingAddress)
class ShippingAddressAdmin(admin.ModelAdmin):
    list_display = (
        'full_name', 'user', 'phone_number',
        'country', 'province', 'city', 'is_default', 'created_at'
    )
    list_filter = ('is_default', 'country', 'province')
    search_fields = ('full_name', 'phone_number', 'street_address', 'user__email')
    list_select_related = ('user', 'country', 'province', 'city')