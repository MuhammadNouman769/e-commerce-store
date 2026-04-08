"""
=================================================================================
    INVENTORY TRACKING MODELS - BTR Mall Stock Management
    Author: Muhammad Nouman
    Purpose: Warehouse management, stock tracking, inventory levels
    Author: Muhammad Nouman
================================================================================
"""

from django.db import models
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from apps.utils.models import BaseModel
from apps.products.models import ProductVariant, Shop
from django.db import transaction
from django.db.models import F
import uuid

'''
=================================================================================
  1. WAREHOUSE MODEL IMPLEMENTATION
      Purpose: Physical or virtual warehouses where stock is stored
      Features:
        - Shop (ForeignKey to Shop model) - the shop that owns the warehouse
        - Name (CharField) - the name of the warehouse
        - Code (UUIDField) - the code of the warehouse
        - City (CharField) - the city of the warehouse
        - Province (CharField) - the province of the warehouse
        - Postal code (CharField) - the postal code of the warehouse
        - Is main (BooleanField) - whether the warehouse is the main warehouse
=================================================================================
'''

class Warehouse(BaseModel):
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
  2. INVENTORY LEVEL MODEL IMPLEMENTATION
      Purpose: Track stock levels for each variant in each warehouse
      Features:
        - Variant (ForeignKey to ProductVariant model) - the variant that is in the inventory level
        - Warehouse (ForeignKey to Warehouse model) - the warehouse that the inventory level is in
        - Available quantity (PositiveIntegerField) - the available quantity of the variant in the warehouse
        - Reserved quantity (PositiveIntegerField) - the reserved quantity of the variant in the warehouse
        - Total quantity (PositiveIntegerField) - the total quantity of the variant in the warehouse
=================================================================================
'''

class InventoryLevel(BaseModel):
    
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
  3. STOCK MOVEMENT MODEL IMPLEMENTATION
      Purpose: Track all stock movements (sale, return, adjustment)
      Features:
        - Inventory level (ForeignKey to InventoryLevel model) - the inventory level that the stock movement is in
        - Movement type (CharField) - the type of the stock movement (sale, return, adjustment)
        - Quantity (IntegerField) - the quantity of the stock movement
        - Note (TextField) - the note of the stock movement
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