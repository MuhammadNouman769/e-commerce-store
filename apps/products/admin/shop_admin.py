from django.contrib import admin
from apps.products.models import Shop
from apps.products.choices.shop_status_choices import ShopStatusChoices


@admin.register(Shop)
class ShopAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "name",
        "owner",
        "shop_status",
        "is_verified",
        "rating",
        "created_at",
    )

    list_filter = (
        "shop_status",
        "is_verified",
        "created_at",
    )

    search_fields = (
        "name",
        "owner__email",
        "handle",
    )

    readonly_fields = (
        "handle",
        "rating",
        "created_at",
        "updated_at",
    )

    fieldsets = (
        ("Basic Info", {
            "fields": ("owner", "name", "description", "handle")
        }),
        ("Verification", {
            "fields": (
                "shop_status",
                "is_verified",
                "verified_at",
                "rejection_reason"
            )
        }),
        ("Media", {
            "fields": ("logo", "banner")
        }),
        ("Documents", {
            "fields": ("cnic_number", "cnic_front", "cnic_back")
        }),
        ("Stats", {
            "fields": ("rating",)
        }),
    )

    actions = ["approve_shop", "reject_shop"]

    def approve_shop(self, request, queryset):
        queryset.update(
            status=ShopStatusChoices.APPROVED,
            is_verified=True
        )
    approve_shop.short_description = "Approve selected shops"

    def reject_shop(self, request, queryset):
        queryset.update(
            status=ShopStatusChoices.REJECTED,
            is_verified=False
        )
    reject_shop.short_description = "Reject selected shops"