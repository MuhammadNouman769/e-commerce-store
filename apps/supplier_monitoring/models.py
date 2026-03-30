"""
================================================================================
          SUPPLY CHAIN MODELS - Supplier & Procurement Management
================================================================================
Purpose: Manage suppliers, purchase orders, and inventory planning
Author: Muhammad Noman
================================================================================
"""
''' ------------ iMPORTS ------------ '''
from django.db import models
from django.utils.translation import gettext_lazy as _
from apps.utilities.models import BaseModel, TimeStampedModel


'''
================================================================================
    1. SUPPLIER MODEL - Vendor/Supplier Information
        Purpose: Manage all suppliers who provide products to sellers
        Features: Contact info, performance metrics, verification
================================================================================
'''

class Supplier(BaseModel):
    """
    Supplier Model - Track vendors who supply products
    """
    
    class SupplierType(models.TextChoices):
        LOCAL = "local", _("Local Supplier")
        INTERNATIONAL = "international", _("International Supplier")
        MANUFACTURER = "manufacturer", _("Manufacturer")
        DISTRIBUTOR = "distributor", _("Distributor")
    
    # Basic Information
    name = models.CharField(
        max_length=255,
        verbose_name=_("Supplier Name")
    )
    
    code = models.CharField(
        max_length=50,
        unique=True,
        verbose_name=_("Supplier Code"),
        help_text=_("e.g., SUP-001")
    )
    
    supplier_type = models.CharField(
        max_length=20,
        choices=SupplierType.choices,
        default=SupplierType.LOCAL,
        verbose_name=_("Supplier Type")
    )
    
    # Contact
    contact_person = models.CharField(
        max_length=255,
        verbose_name=_("Contact Person")
    )
    
    email = models.EmailField(
        verbose_name=_("Email")
    )
    
    phone = models.CharField(
        max_length=20,
        verbose_name=_("Phone")
    )
    
    address = models.TextField(
        verbose_name=_("Address")
    )
    
    # Performance Metrics
    rating = models.DecimalField(
        max_digits=3,
        decimal_places=2,
        default=0,
        verbose_name=_("Rating")
    )
    
    on_time_delivery_rate = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=100,
        verbose_name=_("On-Time Delivery Rate (%)")
    )
    
    # Status
    is_verified = models.BooleanField(
        default=False,
        verbose_name=_("Verified")
    )
    
    class Meta:
        verbose_name = _("Supplier")
        verbose_name_plural = _("Suppliers")
        indexes = [
            models.Index(fields=["code"], name="supplier_code_idx"),
            models.Index(fields=["-rating"], name="supplier_rating_idx"),
        ]
    
    def __str__(self):
        return f"{self.name} ({self.code})"


'''
================================================================================
    2. SUPPLIER PRODUCT - Products Supplied by Each Supplier
        Purpose: Manage which products come from which supplier
        Features: Supplier-specific info, cost price, lead time, MOQ
================================================================================
'''

class SupplierProduct(BaseModel):
    """
    Supplier Product - Which products come from which supplier
    """
    
    supplier = models.ForeignKey(
        Supplier,
        on_delete=models.CASCADE,
        related_name="products",
        verbose_name=_("Supplier")
    )
    
    product = models.ForeignKey(
        "products.Product",
        on_delete=models.CASCADE,
        related_name="suppliers",
        verbose_name=_("Product")
    )
    
    # Supplier-specific info
    supplier_sku = models.CharField(
        max_length=100,
        blank=True,
        verbose_name=_("Supplier SKU")
    )
    
    cost_price = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        verbose_name=_("Cost Price")
    )
    
    lead_time_days = models.PositiveIntegerField(
        default=7,
        verbose_name=_("Lead Time (Days)"),
        help_text_="Days from order to delivery"
    )
    
    minimum_order_quantity = models.PositiveIntegerField(
        default=1,
        verbose_name=_("Minimum Order Quantity")
    )
    
    is_preferred = models.BooleanField(
        default=False,
        verbose_name=_("Preferred Supplier")
    )
    
    class Meta:
        unique_together = ("supplier", "product")
        verbose_name = _("Supplier Product")
        verbose_name_plural = _("Supplier Products")
    
    def __str__(self):
        return f"{self.supplier.name} → {self.product.title}"


'''
================================================================================
    3. PURCHASE ORDER - Orders Placed to Suppliers
        Purpose: Orders placed with suppliers to restock inventory
        Features: Order status, expected/actual delivery, total amount, notes
================================================================================
'''

class PurchaseOrder(BaseModel):
    """
    Purchase Order - Orders placed with suppliers to restock inventory
    """
    
    class OrderStatus(models.TextChoices):
        DRAFT = "draft", _("Draft")
        SENT = "sent", _("Sent to Supplier")
        CONFIRMED = "confirmed", _("Confirmed")
        PROCESSING = "processing", _("Processing")
        SHIPPED = "shipped", _("Shipped")
        RECEIVED = "received", _("Received")
        CANCELLED = "cancelled", _("Cancelled")
    
    po_number = models.CharField(
        max_length=50,
        unique=True,
        editable=False,
        verbose_name=_("PO Number")
    )
    
    supplier = models.ForeignKey(
        Supplier,
        on_delete=models.PROTECT,
        related_name="purchase_orders",
        verbose_name=_("Supplier")
    )
    
    order_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_("Order Date")
    )
    
    expected_delivery_date = models.DateField(
        verbose_name=_("Expected Delivery Date")
    )
    
    actual_delivery_date = models.DateField(
        null=True,
        blank=True,
        verbose_name=_("Actual Delivery Date")
    )
    
    status = models.CharField(
        max_length=20,
        choices=OrderStatus.choices,
        default=OrderStatus.DRAFT,
        verbose_name=_("Status")
    )
    
    total_amount = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        verbose_name=_("Total Amount")
    )
    
    notes = models.TextField(
        blank=True,
        verbose_name=_("Notes")
    )
    
    class Meta:
        verbose_name = _("Purchase Order")
        verbose_name_plural = _("Purchase Orders")
        ordering = ["-order_date"]
        indexes = [
            models.Index(fields=["po_number"], name="po_number_idx"),
            models.Index(fields=["supplier", "status"], name="po_supplier_idx"),
        ]
    
    def __str__(self):
        return f"PO #{self.po_number} - {self.supplier.name}"
    
    def save(self, *args, **kwargs):
        if not self.po_number:
            from django.utils import timezone
            year = timezone.now().year
            last_po = PurchaseOrder.objects.filter(
                po_number__startswith=f"PO-{year}-"
            ).order_by('-po_number').first()
            
            if last_po:
                last_number = int(last_po.po_number.split('-')[-1])
                new_number = last_number + 1
            else:
                new_number = 1
            
            self.po_number = f"PO-{year}-{new_number:06d}"
        
        super().save(*args, **kwargs)


'''
================================================================================
    4. PURCHASE ORDER ITEM - Individual items in a purchase order
        Purpose: Track each item in a purchase order
        Features: Product, quantity, price, subtotal
================================================================================
'''

class PurchaseOrderItem(BaseModel):
    """
    Purchase Order Item - Individual items in a purchase order
    """
    
    purchase_order = models.ForeignKey(
        PurchaseOrder,
        on_delete=models.CASCADE,
        related_name="items",
        verbose_name=_("Purchase Order")
    )
    
    product = models.ForeignKey(
        "products.Product",
        on_delete=models.PROTECT,
        verbose_name=_("Product")
    )
    
    quantity = models.PositiveIntegerField(
        verbose_name=_("Quantity Ordered")
    )
    
    received_quantity = models.PositiveIntegerField(
        default=0,
        verbose_name=_("Quantity Received")
    )
    
    unit_price = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        verbose_name=_("Unit Price")
    )
    
    total_price = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        verbose_name=_("Total Price")
    )
    
    class Meta:
        verbose_name = _("Purchase Order Item")
        verbose_name_plural = _("Purchase Order Items")
    
    def __str__(self):
        return f"{self.product.title} x {self.quantity}"
    
    def save(self, *args, **kwargs):
        self.total_price = self.quantity * self.unit_price
        super().save(*args, **kwargs)