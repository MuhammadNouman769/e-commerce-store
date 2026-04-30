from django.db import models
import os
from apps.utils.models import BaseModel
from .product import Product
from .option import ProductOptionValue
from apps.utils.models import OrderedModel

""" =================== Product Variant Model ====================== """

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




""" ====================== Variant ===================== """ 

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