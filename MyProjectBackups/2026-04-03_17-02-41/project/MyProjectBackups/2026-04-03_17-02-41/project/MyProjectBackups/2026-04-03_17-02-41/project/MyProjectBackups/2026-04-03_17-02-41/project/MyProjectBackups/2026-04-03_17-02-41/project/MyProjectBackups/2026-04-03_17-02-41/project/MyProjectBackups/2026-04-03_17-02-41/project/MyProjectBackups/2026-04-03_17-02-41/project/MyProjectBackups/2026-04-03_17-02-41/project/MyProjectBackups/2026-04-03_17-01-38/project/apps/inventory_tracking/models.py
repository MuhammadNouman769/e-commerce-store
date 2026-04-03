"""
=================================================================================
INVENTORY TRACKING MODELS - B.Store Stock Management
=================================================================================
Purpose: Warehouse management, stock tracking, inventory levels
Author: Muhammad Nouman
=================================================================================
"""

''' ------------ IMPORTS ------------ '''
from django.db import models
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from apps.utilities.models import BaseModel
from apps.products.models import ProductVariant, Shop
from django.db import transaction
from django.db.models import F
import uuid

'''
=================================================================================
  1. WAREHOUSE MODEL INFORMATION
      Purpose: Physical or virtual warehouses where stock is stored
      Features: Multiple warehouses per product, location tracking
=================================================================================
'''

class Warehouse(BaseModel):
    """
    Every shop can have multiple warehouses.
    Example:
    - Lahore Warehouse
    - Karachi Hub
    """
    shop = models.ForeignKey(
        Shop,
        on_delete=models.CASCADE,
        related_name="warehouses",
    )
    name = models.CharField(
        max_length=255,
        verbose_name=_("Warehouse Name")
    )    
    code = models.UUIDField(
        default=uuid.uuid4,
        editable=False,
        unique=True, 
        verbose_name=_("Warehouse Code")
    )

    city = models.CharField(
        max_length=100
    )
    province = models.CharField(
        max_length=100
    )
    postal_code = models.CharField(
        max_length=10
    )
    
    is_main = models.BooleanField(
        default=False
    )
    
    class Meta:
        indexes = [
            models.Index(fields=["shop"]),
            models.Index(fields=["is_main"]),
        ]
    
    def __str__(self):
        return f"{self.name} ({self.shop.name})"


'''
=================================================================================
  2. INVENTORY LEVEL MODEL INFORMATION
      Purpose: Track stock levels for each variant in each warehouse
      Features: Available stock, incoming stock, stock movements
=================================================================================
'''

class InventoryLevel(BaseModel):
    
   # Every stock of product is tracked in every warehouse like:
   # product shoes size 42
   # warehouse Lahore may 10
   # warehouse Karachi may 20
   # total stock = 30

    variant = models.ForeignKey(
        ProductVariant,
        on_delete=models.CASCADE,
        related_name="inventory_levels",
    )
    
    warehouse = models.ForeignKey(
        "Warehouse",
        on_delete=models.CASCADE,
        related_name="stocks",
    )    
    available_quantity = models.PositiveIntegerField(
        default=0,
        verbose_name=_("Available Quantity")
    )    
    reserved_quantity = models.PositiveIntegerField(
        default=0,
        verbose_name=_("Reserved Quantity")
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["variant", "warehouse"],
                name="unique_variant_warehouse"
            ),
            models.CheckConstraint(
                check=models.Q(available_quantity__gte=0),
                name="available_qty_positive"
            )  
        ]
        indexes = [
            models.Index(fields=["variant"]),
            models.Index(fields=["warehouse"])
        ]
    
    def __str__(self):
        return f"{self.variant} - {self.warehouse}: {self.available_quantity}"
    
    @property
    def total_quantity(self):
        # Return available sellable stock
        return self.available_quantity
    
    def reduce_stock(self, qty):
        # After order placement, reserve stock using DB atomic F() update
        updated = InventoryLevel.objects.filter(
            pk=self.pk,
            available_quantity__gte=qty
        ).update(
            available_quantity=F('available_quantity') - qty,
            reserved_quantity=F('reserved_quantity') + qty
        )
        if not updated:
            raise ValidationError("Not enough stock")
    
    def release(self, qty):
       # If order is canceled, release reserved stock back to available using F()
        updated = InventoryLevel.objects.filter(
            pk=self.pk,
            reserved_quantity__gte=qty
        ).update(
            reserved_quantity=F('reserved_quantity') - qty,
            available_quantity=F('available_quantity') + qty
        )
        if not updated:
            raise ValidationError("Invalid release quantity")
    
    def deduct(self, qty):
        # After order completion, deduct reserved stock using F()
        updated = InventoryLevel.objects.filter(
            pk=self.pk,
            reserved_quantity__gte=qty
        ).update(
            reserved_quantity=F('reserved_quantity') - qty
        )
        if not updated:
            raise ValidationError("Not enough reserved stock")


'''
=================================================================================
  3. STOCK MOVEMENT MODEL INFORMATION
      Purpose: Track all stock movements (inbound, outbound, adjustments)
      Features: Complete audit trail, reason tracking
=================================================================================
'''

class StockMovement(BaseModel):
    
    # Track all stock changes for audit and reconciliation
    
    class Type(models.TextChoices):
        SALE = "sale", _("Sale")
        RETURN = "return", _("Customer Return")
        ADJUSTMENT = "adjustment", _("Manual Adjustment")
        
    inventory = models.ForeignKey(
        "InventoryLevel",
        on_delete=models.CASCADE,
        related_name="movements",
    )    
    movement_type = models.CharField(
        max_length=20,
        choices=Type.choices,
    )
    quantity = models.IntegerField()
    
    note = models.CharField(
        max_length=255,
        blank=True,
        null=True,
    )
    
    class Meta:
        constraints = [
            models.CheckConstraint(
                check=models.Q(quantity__gt=0),
                name="positive_stock_movement"
            )
        ]
    
    def __str__(self):
        return f"{self.movement_type} ({self.quantity})"