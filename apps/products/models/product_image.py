import os
from django.db import models

from .product import Product
from .variant import ProductVariant
from apps.utils.models import OrderedModel

""" =================== Product Imade ==================== """

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

