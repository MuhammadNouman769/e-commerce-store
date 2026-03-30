"""
================================================================================
            INVENTORY TRACKING MODELS - B.Store Stock Management
================================================================================
Purpose: Warehouse management, stock tracking, inventory levels
Author: Muhammad Nouman
================================================================================
"""
''' ------------ iMPORTS ------------ '''
from django.db import models
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from apps.utilities.models import BaseModel
from apps.products.models import ProductVariant

'''
================================================================================
    1. WAREHOUSE MODEL - Storage Locations
       Usage: Physical or virtual warehouses where stock is stored
       Features: Multiple warehouses per product, location tracking
================================================================================
'''

class Warehouse(BaseModel):
    """
    Warehouse Model - Daraz Style
    Physical or virtual storage locations
    """
    
    name = models.CharField(
        max_length=255,
        verbose_name=_("Warehouse Name"),
        help_text=_("e.g., Main Warehouse, Karachi Hub, Lahore Fulfillment Center")
    )
    
    code = models.CharField(
        max_length=50,
        unique=True,
        verbose_name=_("Warehouse Code"),
        help_text=_("Unique identifier for warehouse (e.g., WH-001)")
    )
    
    address = models.TextField(
        blank=True,
        verbose_name=_("Address")
    )
    
    city = models.CharField(
        max_length=100,
        blank=True,
        verbose_name=_("City")
    )
    
    country = models.CharField(
        max_length=100,
        default="Pakistan",
        verbose_name=_("Country")
    )
    
    phone = models.CharField(
        max_length=20,
        blank=True,
        verbose_name=_("Contact Phone")
    )
    
    email = models.EmailField(
        blank=True,
        verbose_name=_("Contact Email")
    )
    
    is_main_warehouse = models.BooleanField(
        default=False,
        verbose_name=_("Main Warehouse"),
        help_text=_("Is this the primary warehouse?")
    )
    
    class Meta:
        verbose_name = _("Warehouse")
        verbose_name_plural = _("Warehouses")
        ordering = ["name"]
        indexes = [
            models.Index(fields=["code"], name="warehouse_code_idx"),
            models.Index(fields=["is_main_warehouse"], name="warehouse_main_idx"),
        ]
    
    def __str__(self):
        return f"{self.name} ({self.code})"
    
    def save(self, *args, **kwargs):
        """Ensure only one main warehouse"""
        if self.is_main_warehouse:
            Warehouse.objects.filter(is_main_warehouse=True).exclude(pk=self.pk).update(is_main_warehouse=False)
        super().save(*args, **kwargs)


'''
================================================================================
    2. INVENTORY ITEM MODEL - Product Stock Reference
       Usage: Links product variants to inventory tracking
       Features: Cost tracking, stock status, low stock alerts
================================================================================
'''

class InventoryItem(BaseModel):
    """
    Inventory Item Model - B.Store
    Links product variants to inventory system
    """
    
    variant = models.OneToOneField(
        ProductVariant,
        on_delete=models.CASCADE,
        related_name="inventory_item",
        verbose_name=_("Product Variant")
    )
    
    # Stock Tracking
    track_inventory = models.BooleanField(
        default=True,
        verbose_name=_("Track Inventory"),
        help_text=_("Enable inventory tracking for this product")
    )
    
    # Cost Information
    cost_price = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        null=True,
        blank=True,
        verbose_name=_("Cost Price"),
        help_text=_("Your cost per unit")
    )
    
    # Stock Alerts
    low_stock_threshold = models.PositiveIntegerField(
        default=10,
        verbose_name=_("Low Stock Threshold"),
        help_text=_("Alert when stock falls below this number")
    )
    
    # Status
    is_available = models.BooleanField(
        default=True,
        verbose_name=_("Is Available"),
        help_text=_("Is this product available for sale?")
    )
    
    class Meta:
        verbose_name = _("Inventory Item")
        verbose_name_plural = _("Inventory Items")
        indexes = [
            models.Index(fields=["variant"], name="inventory_variant_idx"),
            models.Index(fields=["track_inventory"], name="inventory_track_idx"),
        ]
    
    def __str__(self):
        return f"Inventory: {self.variant.product.title} - {self.variant.get_variant_name()}"
    
    @property
    def total_stock(self):
        """Get total stock across all warehouses"""
        total = self.levels.aggregate(total=models.Sum('available_quantity'))['total']
        return total or 0
    
    @property
    def is_low_stock(self):
        """Check if stock is below threshold"""
        return self.total_stock <= self.low_stock_threshold
    
    @property
    def is_out_of_stock(self):
        """Check if product is out of stock"""
        return self.total_stock <= 0
    
    def update_variant_stock(self):
        """Update variant stock quantity from inventory levels"""
        if self.track_inventory:
            self.variant.stock_quantity = self.total_stock
            self.variant.save(update_fields=['stock_quantity'])
    
    def allocate_stock(self, warehouse, quantity):
        """Allocate stock from a specific warehouse"""
        level = InventoryLevel.objects.get_or_create(
            inventory_item=self,
            warehouse=warehouse
        )[0]
        
        if level.available_quantity >= quantity:
            level.available_quantity -= quantity
            level.save()
            self.update_variant_stock()
            return True
        return False


'''
================================================================================
    3. INVENTORY LEVEL MODEL - Stock per Warehouse
       Usage: Track stock levels for each variant in each warehouse
       Features: Available stock, incoming stock, stock movements
================================================================================
'''

class InventoryLevel(BaseModel):
    """
    Inventory Level Model - B.Store
    Tracks stock for each variant in each warehouse
    """
    
    inventory_item = models.ForeignKey(
        InventoryItem,
        on_delete=models.CASCADE,
        related_name="levels",
        verbose_name=_("Inventory Item")
    )
    
    warehouse = models.ForeignKey(
        Warehouse,
        on_delete=models.CASCADE,
        related_name="inventory_levels",
        verbose_name=_("Warehouse")
    )
    
    # Stock Quantities
    available_quantity = models.PositiveIntegerField(
        default=0,
        verbose_name=_("Available Quantity"),
        help_text=_("Currently available for sale")
    )
    
    incoming_quantity = models.PositiveIntegerField(
        default=0,
        verbose_name=_("Incoming Quantity"),
        help_text=_("Expected to arrive (in transit)")
    )
    
    reserved_quantity = models.PositiveIntegerField(
        default=0,
        verbose_name=_("Reserved Quantity"),
        help_text=_("Reserved for pending orders")
    )
    
    # Location within warehouse
    bin_location = models.CharField(
        max_length=100,
        blank=True,
        verbose_name=_("Bin Location"),
        help_text=_("Specific location within warehouse")
    )
    
    class Meta:
        unique_together = ("inventory_item", "warehouse")
        verbose_name = _("Inventory Level")
        verbose_name_plural = _("Inventory Levels")
        indexes = [
            models.Index(fields=["inventory_item"], name="level_item_idx"),
            models.Index(fields=["warehouse"], name="level_warehouse_idx"),
            models.Index(fields=["available_quantity"], name="level_quantity_idx"),
        ]
    
    def __str__(self):
        return f"{self.inventory_item.variant.product.title} - {self.warehouse.name}: {self.available_quantity} units"
    
    @property
    def total_quantity(self):
        """Total quantity including incoming"""
        return self.available_quantity + self.incoming_quantity
    
    def reduce_stock(self, quantity):
        """Reduce available stock"""
        if self.available_quantity >= quantity:
            self.available_quantity -= quantity
            self.save()
            self.inventory_item.update_variant_stock()
            return True
        return False
    
    def increase_stock(self, quantity):
        """Increase available stock"""
        self.available_quantity += quantity
        self.save()
        self.inventory_item.update_variant_stock()
    
    def reserve_stock(self, quantity):
        """Reserve stock for order"""
        if self.available_quantity >= quantity:
            self.available_quantity -= quantity
            self.reserved_quantity += quantity
            self.save()
            return True
        return False
    
    def release_reserved_stock(self, quantity):
        """Release reserved stock"""
        if self.reserved_quantity >= quantity:
            self.reserved_quantity -= quantity
            self.available_quantity += quantity
            self.save()
            return True
        return False


'''
================================================================================
    4. STOCK MOVEMENT MODEL - Audit Trail
       Usage: Track all stock movements (inbound, outbound, adjustments)
       Features: Complete audit trail, reason tracking
================================================================================
'''

class StockMovement(BaseModel):
    """
    Stock Movement Model - B.Store
    Track all stock changes for audit and reconciliation
    """
    
    class MovementType(models.TextChoices):
        PURCHASE = "purchase", _("Purchase Order")
        SALE = "sale", _("Sale")
        RETURN = "return", _("Customer Return")
        ADJUSTMENT = "adjustment", _("Manual Adjustment")
        TRANSFER = "transfer", _("Warehouse Transfer")
        DAMAGE = "damage", _("Damaged Stock")
        
    inventory_level = models.ForeignKey(
        InventoryLevel,
        on_delete=models.CASCADE,
        related_name="movements",
        verbose_name=_("Inventory Level")
    )
    
    movement_type = models.CharField(
        max_length=20,
        choices=MovementType.choices,
        verbose_name=_("Movement Type")
    )
    
    quantity = models.IntegerField(
        verbose_name=_("Quantity"),
        help_text=_("Positive = inbound, Negative = outbound")
    )
    
    previous_quantity = models.PositiveIntegerField(
        verbose_name=_("Previous Quantity"),
        help_text=_("Quantity before movement")
    )
    
    new_quantity = models.PositiveIntegerField(
        verbose_name=_("New Quantity"),
        help_text=_("Quantity after movement")
    )
    
    reference_id = models.CharField(
        max_length=100,
        blank=True,
        verbose_name=_("Reference ID"),
        help_text=_("Order ID, Purchase Order ID, etc.")
    )
    
    reason = models.TextField(
        blank=True,
        verbose_name=_("Reason"),
        help_text=_("Reason for stock movement")
    )
    
    performed_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="stock_movements",
        verbose_name=_("Performed By")
    )
    
    class Meta:
        verbose_name = _("Stock Movement")
        verbose_name_plural = _("Stock Movements")
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["inventory_level"], name="movement_level_idx"),
            models.Index(fields=["movement_type"], name="movement_type_idx"),
            models.Index(fields=["reference_id"], name="movement_reference_idx"),
            models.Index(fields=["-created_at"], name="movement_date_idx"),
        ]
    
    def __str__(self):
        sign = "+" if self.quantity > 0 else ""
        return f"{self.movement_type}: {sign}{self.quantity} units - {self.created_at.strftime('%Y-%m-%d')}"