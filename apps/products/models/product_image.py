import os
from django.db import models

from apps.utils.models import OrderedModel
from .product import Product
from .variant import ProductVariant


"""
=========================================================================
5. PRODUCT IMAGE MODEL IMPLEMENTATION
   Usage: Represents an image of a product
   Features:
        - Product (ForeignKey to Product model) - the product that the image belongs to
        - Image (ImageField) - the image of the product
        - Alt text (CharField) - the alt text of the image
        - Position (PositiveSmallIntegerField) - the position of the image
=========================================================================
"""

class ProductImage(OrderedModel):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="images")
    image = models.ImageField(upload_to="products/gallery/%Y/%m/")
    alt_text = models.CharField(max_length=255, blank=True)

    class Meta:
        ordering = ["position"]

    def delete(self, *args, **kwargs):
        if self.image and os.path.isfile(self.image.path):
            os.remove(self.image.path)
        super().delete(*args, **kwargs)


"""
=========================================================================
6. VARIANT IMAGE MODEL IMPLEMENTATION
   Usage: Represents an image of a variant
   Features:
        - Variant (ForeignKey to ProductVariant model) - the variant that the image belongs to
        - Image (ImageField) - the image of the variant
        - Alt text (CharField) - the alt text of the image
        - Position (PositiveSmallIntegerField) - the position of the image
        - Is main (BooleanField) - whether the image is the main image of the variant
=========================================================================
"""

class VariantImage(OrderedModel):
    variant = models.ForeignKey(ProductVariant, on_delete=models.CASCADE, related_name="variant_images")
    image = models.ImageField(upload_to="variants/gallery/%Y/%m/")
    alt_text = models.CharField(max_length=255, blank=True)
    is_main = models.BooleanField(default=False)

    class Meta:
        ordering = ["position"]

    def save(self, *args, **kwargs):
        if self.is_main:
            VariantImage.objects.filter(
                variant=self.variant,
                is_main=True
            ).exclude(pk=self.pk).update(is_main=False)
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        if self.image and os.path.isfile(self.image.path):
            os.remove(self.image.path)
        super().delete(*args, **kwargs)