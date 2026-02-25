from django.db import models

class Product(models.Model):
    shop = models.ForeignKey(
        "Shop",
        on_delete=models.CASCADE,
        related_name="products"
    )

    title = models.CharField(max_length=255)
    handle = models.SlugField(max_length=255)
    description_html = models.TextField(blank=True)

    vendor = models.CharField(max_length=255, blank=True)
    product_type = models.CharField(max_length=255, blank=True)

    status = models.PositiveSmallIntegerField()
    published_at = models.DateTimeField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ("shop", "handle")
        indexes = [
            models.Index(fields=["shop", "status"]),
        ]


class ProductOption(models.Model):
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="options"
    )

    name = models.CharField(max_length=100)
    position = models.PositiveSmallIntegerField()

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ("product", "name")
        ordering = ["position"]



class ProductOptionValue(models.Model):
    option = models.ForeignKey(
        ProductOption,
        on_delete=models.CASCADE,
        related_name="values"
    )

    value = models.CharField(max_length=100)
    position = models.PositiveSmallIntegerField()

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ("option", "value")
        ordering = ["position"]




class ProductVariant(models.Model):
    product = models.ForeignKey(
        "Product",
        on_delete=models.CASCADE,
        related_name="variants"
    )

    # Identity
    sku = models.CharField(max_length=100)
    barcode = models.CharField(max_length=100, blank=True)

    # Pricing
    price = models.DecimalField(max_digits=12, decimal_places=2)
    compare_at_price = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        null=True,
        blank=True
    )

    # Physical properties
    weight = models.DecimalField(
        max_digits=10,
        decimal_places=3,
        null=True,
        blank=True
    )

    # Option combination (denormalized for performance)
    option1 = models.CharField(max_length=100, blank=True)
    option2 = models.CharField(max_length=100, blank=True)
    option3 = models.CharField(max_length=100, blank=True)

    position = models.PositiveSmallIntegerField(default=1)

    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = (
            "product",
            "option1",
            "option2",
            "option3",
        )
        indexes = [
            models.Index(fields=["sku"]),
            models.Index(fields=["product"]),
        ]

    def __str__(self):
        return f"{self.product.title} - {self.sku}"
    


# --------------------------
# Inventory Item (links variant to stock)
# --------------------------
class InventoryItem(models.Model):
    variant = models.OneToOneField(ProductVariant, related_name='inventory_item', on_delete=models.CASCADE)
    sku = models.CharField(max_length=100)  # can mirror variant SKU
    barcode = models.CharField(max_length=100, blank=True)
    tracked = models.BooleanField(default=True)
    cost_price = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

# --------------------------
# Inventory Level (per location)
# --------------------------
class InventoryLevel(models.Model):
    inventory_item = models.ForeignKey(InventoryItem, related_name='levels', on_delete=models.CASCADE)
    location = models.ForeignKey("Warehouse", on_delete=models.CASCADE)  # assume Warehouse model exists
    available_quantity = models.IntegerField(default=0)
    incoming_quantity = models.IntegerField(default=0)

    class Meta:
        unique_together = ('inventory_item', 'location')