from django.contrib import admin
from .models.shop import Shop


@admin.register(Shop)
class ShopAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "owner", "status"]

    actions = ["approve_shop"]

    def approve_shop(self, request, queryset):
        queryset.update(status="approved", is_verified=True)