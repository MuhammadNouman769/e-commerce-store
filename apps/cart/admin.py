from django.contrib import admin

from .models import Address


@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "country", "province", "city", "street", "created_at")
    list_select_related = ("user", "country", "province", "city")
    search_fields = ("street", "user__email", "user__phone")
