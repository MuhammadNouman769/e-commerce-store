from django.db import models

from apps.utils.models import OrderedModel
from .product import Product


"""
=========================================================================
7. PRODUCT OPTION MODEL IMPLEMENTATION
   Usage: Represents an option of a product
   Features:
        - Product (ForeignKey to Product model) - the product that the option belongs to
        - Name (CharField) - the name of the option
        - Position (PositiveSmallIntegerField) - the position of the option
=========================================================================
"""

class ProductOption(OrderedModel):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="options")
    name = models.CharField(max_length=100)

    class Meta:
        unique_together = ("product", "name")

    def __str__(self):
        return f"{self.product.title} - {self.name}"


"""
=========================================================================
8. PRODUCT OPTION VALUE MODEL IMPLEMENTATION
   Usage: Represents a value of an option
   Features:
        - Option (ForeignKey to ProductOption model) - the option that the value belongs to
        - Value (CharField) - the value of the option
        - Position (PositiveSmallIntegerField) - the position of the value
=========================================================================
"""

class ProductOptionValue(OrderedModel):
    option = models.ForeignKey(ProductOption, on_delete=models.CASCADE, related_name="values")
    value = models.CharField(max_length=100)

    class Meta:
        unique_together = ("option", "value")

    def __str__(self):
        return f"{self.option.name}: {self.value}"