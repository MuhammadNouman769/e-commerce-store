""" ============== Order/Fulfillment Models (Improved) =============== """
from django.conf import settings
from django.db import models
from django.core.exceptions import ValidationError
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
import uuid

from apps.cart.models import Cart, ShippingAddress
from apps.utilities.models import BaseModel
from apps.products.models import Product, ProductVariant


class Order(BaseModel):
    """
    Main Order Model - Renamed from BillingDetail
    """
    
    # Order Status Choices
    class OrderStatus(models.TextChoices):
        PENDING = "pending", _("Pending Payment")
        PROCESSING = "processing", _("Processing")
        CONFIRMED = "confirmed", _("Confirmed")
        SHIPPED = "shipped", _("Shipped")
        DELIVERED = "delivered", _("Delivered")
        CANCELLED = "cancelled", _("Cancelled")
        REFUNDED = "refunded", _("Refunded")
        FAILED = "failed", _("Failed")
    
    # Payment Method Choices
    class PaymentMethods(models.TextChoices):
        CARD = "card", _("Credit/Debit Card")
        PAYPAL = "paypal", _("PayPal")
        BANK = "bank", _("Bank Transfer")
        COD = "cod", _("Cash on Delivery")
        STRIPE = "stripe", _("Stripe")
        RAZORPAY = "razorpay", _("Razorpay")
    
    # Payment Status Choices
    class PaymentStatus(models.TextChoices):
        PENDING = "pending", _("Pending")
        PAID = "paid", _("Paid")
        FAILED = "failed", _("Failed")
        REFUNDED = "refunded", _("Refunded")
        PARTIALLY_REFUNDED = "partially_refunded", _("Partially Refunded")
    
    # Order Number (Unique identifier)
    order_number = models.CharField(
        max_length=20,
        unique=True,
        editable=False,
        verbose_name=_("Order Number"),
        help_text=_("Unique order reference number")
    )
    
    # User and Cart Reference
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.PROTECT,  # Don't delete orders if user is deleted
        related_name="orders",
        verbose_name=_("User")
    )
    
    # Keep cart snapshot, but don't cascade delete
    cart = models.ForeignKey(
        Cart, 
        on_delete=models.SET_NULL,  # If cart is deleted, keep order
        null=True, 
        blank=True, 
        related_name="orders",
        verbose_name=_("Original Cart")
    )
    
    # Addresses
    shipping_address = models.ForeignKey(
        ShippingAddress, 
        on_delete=models.PROTECT,  # Don't delete address if used in order
        related_name="orders",
        verbose_name=_("Shipping Address")
    )
    
    # Billing address (if different from shipping)
    billing_address = models.ForeignKey(
        ShippingAddress, 
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name="billing_orders",
        verbose_name=_("Billing Address")
    )
    
    # Order Status
    order_status = models.CharField(
        max_length=20,
        choices=OrderStatus.choices,
        default=OrderStatus.PENDING,
        verbose_name=_("Order Status")
    )
    
    # Payment Details
    payment_method = models.CharField(
        max_length=20, 
        choices=PaymentMethods.choices, 
        default=PaymentMethods.COD,
        verbose_name=_("Payment Method")
    )
    
    payment_status = models.CharField(
        max_length=20,
        choices=PaymentStatus.choices,
        default=PaymentStatus.PENDING,
        verbose_name=_("Payment Status")
    )
    
    transaction_id = models.CharField(
        max_length=100, 
        blank=True, 
        null=True,
        verbose_name=_("Transaction ID"),
        help_text=_("Payment gateway transaction ID")
    )
    
    payment_gateway_response = models.JSONField(
        null=True,
        blank=True,
        verbose_name=_("Payment Gateway Response"),
        help_text=_("Raw response from payment gateway")
    )
    
    # Amounts
    subtotal = models.DecimalField(
        max_digits=12, 
        decimal_places=2,
        verbose_name=_("Subtotal")
    )
    
    tax = models.DecimalField(
        max_digits=12, 
        decimal_places=2, 
        default=0,
        verbose_name=_("Tax")
    )
    
    shipping_fee = models.DecimalField(
        max_digits=12, 
        decimal_places=2, 
        default=0,
        verbose_name=_("Shipping Fee")
    )
    
    discount = models.DecimalField(
        max_digits=12, 
        decimal_places=2, 
        default=0,
        verbose_name=_("Discount")
    )
    
    total_amount = models.DecimalField(
        max_digits=12, 
        decimal_places=2,
        verbose_name=_("Total Amount")
    )
    
    # Timestamps
    paid_at = models.DateTimeField(
        null=True, 
        blank=True,
        verbose_name=_("Paid At")
    )
    
    shipped_at = models.DateTimeField(
        null=True, 
        blank=True,
        verbose_name=_("Shipped At")
    )
    
    delivered_at = models.DateTimeField(
        null=True, 
        blank=True,
        verbose_name=_("Delivered At")
    )
    
    cancelled_at = models.DateTimeField(
        null=True, 
        blank=True,
        verbose_name=_("Cancelled At")
    )
    
    # Shipping Tracking
    tracking_number = models.CharField(
        max_length=100,
        blank=True,
        verbose_name=_("Tracking Number")
    )
    
    courier_company = models.CharField(
        max_length=100,
        blank=True,
        verbose_name=_("Courier Company")
    )
    
    tracking_url = models.URLField(
        blank=True,
        verbose_name=_("Tracking URL")
    )
    
   # Customer Notes
    customer_notes = models.TextField(
        blank=True,
        verbose_name=_("Customer Notes"),
        help_text=_("Special instructions from customer")  # ← Fix here
    )

    admin_notes = models.TextField(
        blank=True,
        verbose_name=_("Admin Notes"),
        help_text=_("Internal notes for staff")  # ← Also check this
    )
    
    # For discount codes/coupons
    coupon_code = models.CharField(
        max_length=50,
        blank=True,
        verbose_name=_("Coupon Code")
    )
    
    class Meta:
        verbose_name = _("Order")
        verbose_name_plural = _("Orders")
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["order_number"]),
            models.Index(fields=["user", "order_status"]),
            models.Index(fields=["order_status", "created_at"]),
            models.Index(fields=["payment_status"]),
            models.Index(fields=["shipping_address"]),
        ]

    def __str__(self):
        return f"Order #{self.order_number} - {self.user.email} - {self.order_status}"
    
    def save(self, *args, **kwargs):
        """Auto-generate order number and handle timestamps"""
        if not self.order_number:
            # Generate unique order number: ORD-2024-0001 format
            year = timezone.now().year
            last_order = Order.objects.filter(
                order_number__startswith=f"ORD-{year}-"
            ).order_by('-order_number').first()
            
            if last_order:
                last_number = int(last_order.order_number.split('-')[-1])
                new_number = last_number + 1
            else:
                new_number = 1
            
            self.order_number = f"ORD-{year}-{new_number:06d}"
        
        # Update timestamps based on status
        if self.order_status == self.OrderStatus.PAID and not self.paid_at:
            self.paid_at = timezone.now()
        elif self.order_status == self.OrderStatus.SHIPPED and not self.shipped_at:
            self.shipped_at = timezone.now()
        elif self.order_status == self.OrderStatus.DELIVERED and not self.delivered_at:
            self.delivered_at = timezone.now()
        elif self.order_status == self.OrderStatus.CANCELLED and not self.cancelled_at:
            self.cancelled_at = timezone.now()
        
        super().save(*args, **kwargs)
    
    @property
    def is_paid(self):
        """Check if order is paid"""
        return self.payment_status == self.PaymentStatus.PAID
    
    @property
    def is_delivered(self):
        """Check if order is delivered"""
        return self.order_status == self.OrderStatus.DELIVERED
    
    @property
    def can_cancel(self):
        """Check if order can be cancelled"""
        return self.order_status in [
            self.OrderStatus.PENDING,
            self.OrderStatus.PROCESSING
        ]
    
    def calculate_total(self):
        """Recalculate total amount"""
        total = self.subtotal + self.tax + self.shipping_fee - self.discount
        return total
    
    def mark_as_paid(self, transaction_id=None, gateway_response=None):
        """Mark order as paid"""
        self.payment_status = self.PaymentStatus.PAID
        self.order_status = self.OrderStatus.PROCESSING
        self.paid_at = timezone.now()
        if transaction_id:
            self.transaction_id = transaction_id
        if gateway_response:
            self.payment_gateway_response = gateway_response
        self.save()
    
    def mark_as_shipped(self, tracking_number=None, courier=None):
        """Mark order as shipped"""
        self.order_status = self.OrderStatus.SHIPPED
        self.shipped_at = timezone.now()
        if tracking_number:
            self.tracking_number = tracking_number
        if courier:
            self.courier_company = courier
        self.save()
    
    def mark_as_delivered(self):
        """Mark order as delivered"""
        self.order_status = self.OrderStatus.DELIVERED
        self.delivered_at = timezone.now()
        self.save()
    
    def cancel_order(self, reason=""):
        """Cancel order"""
        self.order_status = self.OrderStatus.CANCELLED
        self.cancelled_at = timezone.now()
        if reason:
            self.admin_notes = f"Cancelled: {reason}\n{self.admin_notes}"
        self.save()


class OrderItem(BaseModel):
    """
    Individual items in an order (Line Items)
    """
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name="items",
        verbose_name=_("Order")
    )
    
    product = models.ForeignKey(
        Product,
        on_delete=models.PROTECT,
        related_name="order_items",
        verbose_name=_("Product")
    )
    
    variant = models.ForeignKey(
        ProductVariant,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name="order_items",
        verbose_name=_("Variant")
    )
    
    # Snapshot fields (in case product changes later)
    product_name = models.CharField(
        max_length=255,
        verbose_name=_("Product Name")
    )
    
    variant_name = models.CharField(
        max_length=255,
        blank=True,
        verbose_name=_("Variant Name")
    )
    
    sku = models.CharField(
        max_length=100,
        blank=True,
        verbose_name=_("SKU")
    )
    
    quantity = models.PositiveIntegerField(
        verbose_name=_("Quantity")
    )
    
    price = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        verbose_name=_("Unit Price")
    )
    
    total_price = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        verbose_name=_("Total Price")
    )
    
    # For returns/refunds
    returned_quantity = models.PositiveIntegerField(
        default=0,
        verbose_name=_("Returned Quantity")
    )
    
    refund_amount = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0,
        verbose_name=_("Refund Amount")
    )
    
    class Meta:
        verbose_name = _("Order Item")
        verbose_name_plural = _("Order Items")
        ordering = ["id"]
        indexes = [
            models.Index(fields=["order"]),
            models.Index(fields=["product"]),
        ]
    
    def __str__(self):
        variant_text = f" - {self.variant_name}" if self.variant_name else ""
        return f"{self.product_name}{variant_text} x {self.quantity}"
    
    def save(self, *args, **kwargs):
        """Auto-calculate total price"""
        self.total_price = self.quantity * self.price
        super().save(*args, **kwargs)
    
    @property
    def is_fully_returned(self):
        """Check if item is fully returned"""
        return self.returned_quantity >= self.quantity
    
    def return_item(self, quantity, refund_amount=None):
        """Return item"""
        if quantity > (self.quantity - self.returned_quantity):
            raise ValidationError(_("Cannot return more than purchased quantity"))
        
        self.returned_quantity += quantity
        if refund_amount:
            self.refund_amount = refund_amount
        else:
            self.refund_amount = quantity * self.price
        self.save()


class OrderHistory(BaseModel):
    """
    Track order status changes and actions
    """
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name="history",
        verbose_name=_("Order")
    )
    
    status_from = models.CharField(
        max_length=20,
        blank=True,
        verbose_name=_("Status From")
    )
    
    status_to = models.CharField(
        max_length=20,
        verbose_name=_("Status To")
    )
    
    action = models.CharField(
        max_length=100,
        verbose_name=_("Action"),
        help_text=_("What action was performed")
    )
    
    performed_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="order_actions",
        verbose_name=_("Performed By")
    )
    
    notes = models.TextField(
        blank=True,
        verbose_name=_("Notes")
    )
    
    ip_address = models.GenericIPAddressField(
        null=True,
        blank=True,
        verbose_name=_("IP Address")
    )
    
    class Meta:
        verbose_name = _("Order History")
        verbose_name_plural = _("Order Histories")
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["order"]),
            models.Index(fields=["status_to", "created_at"]),
        ]
    
    def __str__(self):
        return f"Order #{self.order.order_number} - {self.action} - {self.created_at}"
    
    def save(self, *args, **kwargs):
        """Auto-set status from/to"""
        if not self.status_from and self.order:
            # Get previous status from last history entry
            last_history = OrderHistory.objects.filter(
                order=self.order
            ).exclude(pk=self.pk).order_by('-created_at').first()
            if last_history:
                self.status_from = last_history.status_to
        
        super().save(*args, **kwargs)


# Keep original model for backward compatibility (deprecated)
class BillingDetail(BaseModel):
    """DEPRECATED: Use Order model instead"""

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

    paid_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = _("Billing Detail (Deprecated)")
        verbose_name_plural = _("Billing Details (Deprecated)")

    def __str__(self):
        return f"Billing for Cart #{self.cart_id} - {self.user_id}"