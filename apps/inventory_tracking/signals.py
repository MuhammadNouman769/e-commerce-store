'''
================================================================================
    INVENTORY TRACKING SIGNALS - Warehouse and Stock Management
================================================================================
    Purpose: Handle automatic warehouse management and inventory synchronization
    Author: Muhammad Nouman
================================================================================
'''
''' ------------------- WAREHOUSE AND STOCK MOVEMENT ------------------- '''
from django.db.models.signals import pre_save, post_delete
from django.dispatch import receiver
from .models import Warehouse, InventoryLevel


# 1. Auto-handle is_main warehouse
@receiver(pre_save, sender=Warehouse)
def ensure_single_main_warehouse(sender, instance, **kwargs):
    #  Ensure that only one warehouse per shop is main.
    #  If instance.is_main=True, set others to False automatically.
    if instance.is_main:
        Warehouse.objects.filter(shop=instance.shop, is_main=True).exclude(pk=instance.pk).update(is_main=False)

# 2️ Inventory sync on warehouse delete
@receiver(post_delete, sender=Warehouse)
def handle_warehouse_delete(sender, instance, **kwargs):
    # When a warehouse is deleted, adjust or log inventory for all variants in this warehouse.
    # This is a placeholder – can be customized to:
    # - Deduct stock
    # - Move stock to main warehouse
    # - Generate alerts
    
    # Example: just print affected variants
    variants = InventoryLevel.objects.filter(warehouse=instance)
    for inv in variants:
        print(f"Warehouse deleted: {instance.name}, Variant: {inv.variant}, Qty: {inv.available_quantity}")
    # Optional: update inventory, move stock, or notify