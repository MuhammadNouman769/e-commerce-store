from django.db import models

from apps.utils.models import BaseModel
from .product import Product
from .option import ProductOptionValue


"""
=========================================================================
2. PRODUCT VARIANT MODEL IMPLEMENTATION
   Usage: Represents a variant of a product with different options and pricing
   Features:
        - Product (ForeignKey to Product model) - the product that the variant belongs to
        - Sku (CharField) - the stock keeping unit of the variant
        - Barcode (CharField) - the barcode of the variant
        - Option1 (ForeignKey to ProductOptionValue model) - the first option of the variant
        - Option2 (ForeignKey to ProductOptionValue model) - the second option of the variant
        - Option3 (ForeignKey to ProductOptionValue model) - the third option of the variant
        - Price (DecimalField) - the price of the variant
        - Compare at price (DecimalField) - the compare at price of the variant
        - Stock quantity (PositiveIntegerField) - the stock quantity of the variant
        - Track inventory (BooleanField) - whether the inventory is tracked for the variant
        - Allow backorder (BooleanField) - whether the backorder is allowed for the variant
        - Position (PositiveSmallIntegerField) - the position of the variant
=========================================================================
"""

class ProductVariant(BaseModel):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="variants")

    sku = models.CharField(max_length=100, unique=True, null=True, blank=True)
    barcode = models.CharField(max_length=100, unique=True, null=True, blank=True)

    option1 = models.ForeignKey(ProductOptionValue, on_delete=models.CASCADE, null=True, blank=True, related_name="variants_option1")
    option2 = models.ForeignKey(ProductOptionValue, on_delete=models.CASCADE, null=True, blank=True, related_name="variants_option2")
    option3 = models.ForeignKey(ProductOptionValue, on_delete=models.CASCADE, null=True, blank=True, related_name="variants_option3")

    price = models.DecimalField(max_digits=12, decimal_places=2)
    compare_at_price = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)

    stock_quantity = models.PositiveIntegerField(default=0)
    track_inventory = models.BooleanField(default=False)
    allow_backorder = models.BooleanField(default=False)

    position = models.PositiveSmallIntegerField(default=0)

    def get_variant_name(self):
        values = [o.value for o in [self.option1, self.option2, self.option3] if o]
        return " / ".join(values) if values else None

    @property
    def is_in_stock(self):
        if not self.track_inventory:
            return True
        if self.allow_backorder:
            return True
        return self.stock_quantity > 0

    def __str__(self):
        return f"{self.product.title} - {self.get_variant_name() or self.sku or 'Base'}"