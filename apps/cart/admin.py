from django.contrib import admin

from .models import Address, Cart, CartItem, ShippingAddress


@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "country", "province", "city", "street", "created_at")
    list_select_related = ("user", "country", "province", "city")
    search_fields = ("street", "user__email", "user__phone")


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "is_active", "created_at", "updated_at")
    list_select_related = ("user",)
    search_fields = ("user__email",)


@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ("id", "cart", "product_name", "quantity", "price", "created_at")
    list_select_related = ("cart", "cart__user")
    search_fields = ("product_name", "cart__user__email")


@admin.register(ShippingAddress)
class ShippingAddressAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "user",
        "full_name",
        "phone_number",
        "country",
        "province",
        "city",
        "postal_code",
        "is_default",
        "created_at",
    )
    list_select_related = ("user", "country", "province", "city")
    search_fields = ("full_name", "phone_number", "street_address", "user__email")
