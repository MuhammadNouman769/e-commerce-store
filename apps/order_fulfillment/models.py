''' 
================================================================================
    ORDER FULFILLMENT MODELS - BTR Mall Order Fulfillment
    Purpose: Track individual shipments from warehouse to customer
    Author: Muhammad Nouman
================================================================================
'''
'''============= IMPORTING MODELS ============='''

from django.conf import settings
from django.db import models, transaction
from django.core.exceptions import ValidationError
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from decimal import Decimal

from apps.cart.models import Cart, ShippingAddress
from apps.utils.models import BaseModel
from apps.products.models import Product, ProductVariant


'''
=============================================================================
    1.  ORDER MODEL IMPLEMENTATION
      Purpose: Track individual shipments from warehouse to customer
      Features:
        - Order number (CharField) - the order number
        - User (ForeignKey to User model) - the user who owns the order
        - Cart (ForeignKey to Cart model) - the cart that the order is from
        - Shipping address (ForeignKey to ShippingAddress model) - the shipping address for the order
        - Billing address (ForeignKey to ShippingAddress model) - the billing address for the order
        - Order status (CharField) - the status of the order
        - Payment method (CharField) - the method of payment used for the order
        - Payment status (CharField) - the status of the payment
============================================================================='''

class Order(BaseModel):

    class OrderStatus(models.TextChoices):
        PENDING = "pending", _("Pending Payment")
        PROCESSING = "processing", _("Processing")
        CONFIRMED = "confirmed", _("Confirmed")
        SHIPPED = "shipped", _("Shipped")
        DELIVERED = "delivered", _("Delivered")
        CANCELLED = "cancelled", _("Cancelled")
        REFUNDED = "refunded", _("Refunded")
        FAILED = "failed", _("Failed")

    class PaymentMethods(models.TextChoices):
        CARD = "card", _("Credit/Debit Card")
        PAYPAL = "paypal", _("PayPal")
        BANK = "bank", _("Bank Transfer")
        COD = "cod", _("Cash on Delivery")
        STRIPE = "stripe", _("Stripe")
        RAZORPAY = "razorpay", _("Razorpay")

    class PaymentStatus(models.TextChoices):
        PENDING = "pending", _("Pending")
        PAID = "paid", _("Paid")
        FAILED = "failed", _("Failed")
        REFUNDED = "refunded", _("Refunded")
        PARTIALLY_REFUNDED = "partially_refunded", _("Partially Refunded")

    order_number = models.CharField(max_length=20, unique=True, editable=False)

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="orders"
    )

    cart = models.ForeignKey(
        Cart,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="orders"
    )

    shipping_address = models.ForeignKey(
        ShippingAddress,
        on_delete=models.PROTECT,
        related_name="orders"
    )

    billing_address = models.ForeignKey(
        ShippingAddress,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name="billing_orders"
    )

    order_status = models.CharField(
        max_length=20,
        choices=OrderStatus.choices,
        default=OrderStatus.PENDING,
        db_index=True
    )

    payment_method = models.CharField(
        max_length=20,
        choices=PaymentMethods.choices,
        default=PaymentMethods.COD
    )

    payment_status = models.CharField(
        max_length=20,
        choices=PaymentStatus.choices,
        default=PaymentStatus.PENDING,
        db_index=True
    )

    transaction_id = models.CharField(
        max_length=100, 
        blank=True, 
        null=True
    )

    payment_gateway_response = models.JSONField(
        null=True, 
        blank=True, 
        default=dict
    )

    subtotal = models.DecimalField(
        max_digits=12, 
        decimal_places=2
    )
    tax = models.DecimalField(
        max_digits=12, 
        decimal_places=2, 
        default=Decimal("0.00")
    )
    shipping_fee = models.DecimalField(
        max_digits=12, 
        decimal_places=2, 
        default=Decimal("0.00")
    )
    discount = models.DecimalField(
        max_digits=12, 
        decimal_places=2, 
        default=Decimal("0.00")
    )
    total_amount = models.DecimalField(
        max_digits=12, 
        decimal_places=2
    )

    paid_at = models.DateTimeField(
        null=True, 
        blank=True
    )
    shipped_at = models.DateTimeField(
        null=True, 
        blank=True
    )
    delivered_at = models.DateTimeField(
        null=True, 
        blank=True
    )
    cancelled_at = models.DateTimeField(
        null=True, 
        blank=True
    )

    tracking_number = models.CharField(
        max_length=100, 
        blank=True
    )
    courier_company = models.CharField(
        max_length=100, 
        blank=True
    )
    tracking_url = models.URLField(
        blank=True
    )

    customer_notes = models.TextField(
        max_length=400, 
        blank=True
    )
    admin_notes = models.TextField(
        max_length=400, 
        blank=True
    )
    coupon_code = models.CharField(
        max_length=50, 
        blank=True
    )

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"Order #{self.order_number}"

    def save(self, *args, **kwargs):
        if not self.order_number:
            with transaction.atomic():
                year = timezone.now().year
                last = Order.objects.select_for_update().filter(
                    order_number__startswith=f"ORD-{year}-"
                ).order_by('-order_number').first()

                num = int(last.order_number.split('-')[-1]) + 1 if last else 1
                self.order_number = f"ORD-{year}-{num:06d}"

        self.total_amount = self.subtotal + self.tax + self.shipping_fee - self.discount
        super().save(*args, **kwargs)

    @property
    def is_paid(self):
        return self.payment_status == self.PaymentStatus.PAID

    @property
    def can_cancel(self):
        return self.order_status in [self.OrderStatus.PENDING, self.OrderStatus.PROCESSING]


'''
=============================================================================
     2. ORDER ITEM MODEL IMPLEMENTATION
      Purpose: Track individual shipments from warehouse to customer
      Features:
        - Order (ForeignKey to Order model) - the order that the item belongs to
        - Product (ForeignKey to Product model) - the product that the item is for
        - Variant (ForeignKey to ProductVariant model) - the variant that the item is for
        - Product name (CharField) - the name of the product
        - Variant name (CharField) - the name of the variant
        - SKU (CharField) - the SKU of the product
        - Quantity (PositiveIntegerField) - the quantity of the product
        - Price (DecimalField) - the price of the product
============================================================================='''

class OrderItem(BaseModel):

    order = models.ForeignKey(
        Order, 
        on_delete=models.CASCADE, 
        related_name="items"
    )
    product = models.ForeignKey(
        Product, 
        on_delete=models.PROTECT
    )
    variant = models.ForeignKey(
        ProductVariant, 
        on_delete=models.PROTECT, 
        null=True, 
        blank=True
    )

    product_name = models.CharField(
        max_length=255
    )
    variant_name = models.CharField(
        max_length=255, 
        blank=True
    )
    sku = models.CharField(
        max_length=100, 
        blank=True
    )

    quantity = models.PositiveIntegerField()
    price = models.DecimalField(
        max_digits=12, 
        decimal_places=2
    )
    total_price = models.DecimalField(
        max_digits=12, 
        decimal_places=2
    )

    returned_quantity = models.PositiveIntegerField(default=0)
    refund_amount = models.DecimalField(
        max_digits=12, 
        decimal_places=2, 
        default=Decimal("0.00")
    )

    class Meta:
        ordering = ["id"]

    def save(self, *args, **kwargs):
        self.total_price = Decimal(self.quantity) * Decimal(self.price)
        super().save(*args, **kwargs)


'''
=============================================================================
     3. ORDER HISTORY MODEL IMPLEMENTATION
      Purpose: Track individual shipments from warehouse to customer
      Features:
        - Order (ForeignKey to Order model) - the order that the history belongs to
        - Status from (CharField) - the status of the order from the previous status
        - Status to (CharField) - the status of the order to the new status
        - Action (CharField) - the action that was performed on the order
        - Performed by (ForeignKey to User model) - the user that performed the action
        - Notes (TextField) - the notes of the action
============================================================================='''

class OrderHistory(BaseModel):

    class ActionType(models.TextChoices):
        CREATED = "created"
        STATUS_CHANGED = "status_changed"
        PAYMENT = "payment"
        SHIPPED = "shipped"
        DELIVERED = "delivered"
        CANCELLED = "cancelled"

    order = models.ForeignKey(
        Order, 
        on_delete=models.CASCADE, 
        related_name="history"
    )

    status_from = models.CharField(
        max_length=20, 
        blank=True
    )
    status_to = models.CharField(
        max_length=20
    )

    action = models.CharField(
        max_length=50, 
        choices=ActionType.choices
    )

    performed_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    notes = models.TextField(blank=True)

    def __str__(self):
        return f"{self.order.order_number} - {self.action}"