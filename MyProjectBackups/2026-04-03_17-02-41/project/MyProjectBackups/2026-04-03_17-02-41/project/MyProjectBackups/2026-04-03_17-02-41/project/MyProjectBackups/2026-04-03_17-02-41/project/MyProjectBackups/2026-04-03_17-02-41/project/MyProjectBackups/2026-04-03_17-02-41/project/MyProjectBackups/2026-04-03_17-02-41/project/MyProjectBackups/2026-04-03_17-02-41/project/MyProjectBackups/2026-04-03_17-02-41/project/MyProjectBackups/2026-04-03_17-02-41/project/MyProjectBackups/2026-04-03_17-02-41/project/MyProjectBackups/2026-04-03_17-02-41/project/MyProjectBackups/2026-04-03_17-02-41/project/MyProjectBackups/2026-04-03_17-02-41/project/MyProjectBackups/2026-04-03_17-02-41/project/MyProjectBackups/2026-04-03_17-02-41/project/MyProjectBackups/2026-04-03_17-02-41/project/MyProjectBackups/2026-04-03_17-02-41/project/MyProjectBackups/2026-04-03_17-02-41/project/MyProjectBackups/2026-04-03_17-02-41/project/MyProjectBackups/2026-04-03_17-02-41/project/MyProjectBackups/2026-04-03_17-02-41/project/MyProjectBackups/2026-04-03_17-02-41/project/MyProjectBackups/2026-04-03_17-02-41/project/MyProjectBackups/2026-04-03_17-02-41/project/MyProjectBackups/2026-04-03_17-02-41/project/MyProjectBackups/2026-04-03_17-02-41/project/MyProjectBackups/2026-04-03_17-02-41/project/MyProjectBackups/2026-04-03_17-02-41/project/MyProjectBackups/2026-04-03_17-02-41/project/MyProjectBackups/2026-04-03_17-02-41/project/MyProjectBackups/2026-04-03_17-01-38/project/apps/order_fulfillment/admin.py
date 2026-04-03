from django.contrib import admin

from .models import BillingDetail


@admin.register(BillingDetail)
class BillingDetailAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "cart", "payment_method", "total_amount", "paid_at", "is_active")
    list_select_related = ("user", "cart", "shipping_address")
    search_fields = ("user__email", "cart__id", "transaction_id")
