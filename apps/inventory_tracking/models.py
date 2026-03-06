from django.db import models
from apps.utilities.models import BaseModel
from apps.products.models import ProductVariant
#from apps.inventory_tracking.models import Warehouse, InventoryItem, InventoryLevel


""" ========== Warehouse ============ """
class Warehouse(BaseModel):
    name = models.CharField(max_length=255)
    address = models.TextField(blank=True)

    def __str__(self):
        return self.name

""" =========== Inventory Item and Level =========== """
class InventoryItem(BaseModel):
    variant = models.OneToOneField(ProductVariant, related_name='inventory_item', on_delete=models.CASCADE)
    tracked = models.BooleanField(default=True)
    cost_price = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)

""" InventoryLevel tracks available and incoming stock for each inventory item at each warehouse. """
class InventoryLevel(BaseModel):
    inventory_item = models.ForeignKey(InventoryItem, related_name='levels', on_delete=models.CASCADE)
    warehouse = models.ForeignKey(Warehouse, on_delete=models.CASCADE)
    available_quantity = models.IntegerField(default=0)
    incoming_quantity = models.IntegerField(default=0)

    class Meta:
        unique_together = ('inventory_item', 'warehouse')
        indexes = [
            models.Index(fields=['inventory_item']),
            models.Index(fields=['warehouse']),
        ]