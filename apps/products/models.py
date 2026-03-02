''' =============== Imports =============== '''
from django.db import models
from apps.utilities.models import BaseModel
from django.utils.text import slugify


''' ============== Start Product Model =============== '''
class Product(BaseModel):
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

    class Meta:
        unique_together = ("shop", "handle")
        indexes = [
            models.Index(fields=["shop", "status"]),
        ]
        
''' ------------- End Product Model --------------- '''



''' =============== Start ProductOption Model ============== '''
class ProductOption(BaseModel):
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="options"
    )

    name = models.CharField(max_length=100)
    position = models.PositiveSmallIntegerField()


    class Meta:
        unique_together = ("product", "name")
        ordering = ["position"]

''' ------------ End ProductOption Model ------------- '''


''' ============ Start ProductOptionValue Model ============ '''
class ProductOptionValue(BaseModel):
    option = models.ForeignKey(
        ProductOption,
        on_delete=models.CASCADE,
        related_name="values"
    )

    value = models.CharField(max_length=100)
    position = models.PositiveSmallIntegerField()


    class Meta:
        unique_together = ("option", "value")
        ordering = ["position"]

''' ------------- End ProductOptionValue Model ------------ '''



''' ============= Start ProductVariant Model ============== '''
class ProductVariant(BaseModel):
    product = models.ForeignKey(
        "Product",
        on_delete=models.CASCADE,
        related_name="variants"
    )
    # Identity
    barcode = models.CharField(max_length=100, blank=True)
    sku = models.CharField(max_length=100)

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
    
''' ------------- End ProductVariant ------------- '''

'''



---------------------------------------
Inventory Item (links variant to stock)
----------------------------------------
'''
class InventoryItem(BaseModel):
    variant = models.OneToOneField(ProductVariant, related_name='inventory_item', on_delete=models.CASCADE)
    barcode = models.CharField(max_length=100, blank=True)
    sku = models.CharField(max_length=100)

    tracked = models.BooleanField(default=True)
    cost_price = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)

'''
--------------------------------
 Inventory Level (per location)
--------------------------------
'''
class InventoryLevel(BaseModel):
    inventory_item = models.ForeignKey(InventoryItem, related_name='levels', on_delete=models.CASCADE)
    location = models.ForeignKey("Warehouse", on_delete=models.CASCADE)  # assume Warehouse model exists
    available_quantity = models.IntegerField(default=0)
    incoming_quantity = models.IntegerField(default=0)

    class Meta:
        unique_together = ('inventory_item', 'location')


class Category(BaseModel):
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, blank=True)

    # Self-referencing parent for hierarchy
    parent = models.ForeignKey(
        "self",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="children"
    )

    # Whether the category is active
    is_active = models.BooleanField(default=True)

    # Optional fields for SEO / navigation
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to="category_images/", null=True, blank=True)

    # Position/order for sorting
    position = models.PositiveSmallIntegerField(default=0)


    class Meta:
        verbose_name_plural = "Categories"
        ordering = ["position", "name"]

    def __str__(self):
        return self.name

    # Auto-generate slug if blank
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)