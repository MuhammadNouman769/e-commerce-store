from django.conf import settings
from django.db import models

from apps.cart.models import Cart, ShippingAddress
from apps.utilities.models import BaseModel


class BillingDetail(BaseModel):
    class PaymentMethods(models.TextChoices):
        CARD = "card", "Credit/Debit Card"
        PAYPAL = "paypal", "PayPal"
        BANK = "bank", "Bank Transfer"
        COD = "cod", "Cash on Delivery"

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="billing_details")
    shipping_address = models.ForeignKey(
        ShippingAddress, on_delete=models.SET_NULL, null=True, blank=True, related_name="billing_details"
    )
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name="billing_details")

    payment_method = models.CharField(max_length=20, choices=PaymentMethods.choices, default=PaymentMethods.COD)
    transaction_id = models.CharField(max_length=100, blank=True, null=True)

    subtotal = models.DecimalField(max_digits=12, decimal_places=2)
    tax = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    shipping_fee = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    discount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    total_amount = models.DecimalField(max_digits=12, decimal_places=2)

    # Use BaseModel timestamps, but keep a separate paid timestamp for demo clarity
    paid_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Billing for Cart #{self.cart_id} - {self.user_id}"
